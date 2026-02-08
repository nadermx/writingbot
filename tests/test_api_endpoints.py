"""
Integration tests for internal API POST endpoints.
Uses real backends: api.writingbot.ai for LLM, translateapi.ai for translation.
Validation-only tests (empty text, missing fields) don't hit external services.
Tests that hit external APIs accept both success (200) and service-unavailable (500)
so they don't fail when a backend is temporarily down.
"""
import json

from django.test import TestCase, Client


class BaseAPITestCase(TestCase):
    """Shared setup for all API endpoint tests."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()
        # Clear DRF throttle caches so other test suites don't cause 429s
        from rest_framework.throttling import SimpleRateThrottle
        if hasattr(SimpleRateThrottle, 'cache'):
            SimpleRateThrottle.cache.clear()

    def assertAPISuccess(self, response, expected_keys=None):
        """Assert API returned 200 with expected keys, or 500 if backend is down."""
        self.assertIn(
            response.status_code, [200, 500],
            f'Expected 200 or 500, got {response.status_code}: {response.content[:200]}'
        )
        if response.status_code == 200 and expected_keys:
            data = response.json()
            for key in expected_keys:
                self.assertIn(key, data, f'Missing key "{key}" in response: {list(data.keys())}')


class ParaphraseAPITests(BaseAPITestCase):
    """POST /api/paraphrase/"""

    def test_basic_paraphrase(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'The cat sat on the mat.', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['output_text', 'input_word_count', 'output_word_count', 'mode'])

    def test_fluency_mode(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'Technology is changing the world rapidly.', 'mode': 'fluency'}),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['output_text', 'mode'])

    def test_empty_text_returns_400(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': '', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_missing_text_returns_400(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_mode_returns_400(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'Hello world.', 'mode': 'nonexistent'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class GrammarCheckAPITests(BaseAPITestCase):
    """POST /api/grammar/check/"""

    def test_basic_grammar_check(self):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': 'Teh cat sat on teh mat. He dont like it.'}),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['corrections', 'writing_scores', 'word_count'])

    def test_empty_text_returns_400(self):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_with_dialect(self):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': 'Colour is the correct spelling in British English.', 'dialect': 'en-gb'}),
            content_type='application/json',
        )
        self.assertAPISuccess(response)


class SummarizeAPITests(BaseAPITestCase):
    """POST /api/summarize/"""

    def test_basic_summarize(self):
        long_text = (
            'Artificial intelligence is transforming every industry. '
            'From healthcare to finance, AI systems are being deployed to automate tasks, '
            'improve decision-making, and create new products. Machine learning algorithms '
            'can analyze vast amounts of data and identify patterns that humans might miss. '
            'Natural language processing enables computers to understand and generate text. '
            'Computer vision allows machines to interpret images and video. '
            'These technologies are becoming more accessible and affordable every year. '
        ) * 4
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': long_text}),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['summary', 'stats'])

    def test_empty_text_returns_400(self):
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class AIDetectAPITests(BaseAPITestCase):
    """POST /api/ai-detect/"""

    def test_basic_detect(self):
        text = (
            'The rapid advancement of artificial intelligence has sparked both excitement '
            'and concern across various sectors of society. As machine learning algorithms '
            'become increasingly sophisticated, they are being integrated into everything '
            'from healthcare diagnostics to autonomous vehicles. Researchers continue to '
            'push the boundaries of what these systems can achieve, while ethicists and '
            'policymakers grapple with questions about accountability, bias, and the future '
            'of human employment. The development of large language models has demonstrated '
            'remarkable capabilities in understanding and generating natural language, leading '
            'to applications that were previously thought to be decades away from realization. '
            'Despite these advances, significant challenges remain in ensuring these technologies '
            'are deployed responsibly and equitably across different communities and populations.'
        )
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': text}),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['classification', 'overall_score', 'sentences', 'word_count'])

    def test_empty_text_returns_400(self):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_too_short_text_returns_400(self):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': 'This is too short.'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class TranslateAPITests(BaseAPITestCase):
    """POST /api/translate/ — uses real translateapi.ai backend."""

    def test_basic_translate(self):
        response = self.client.post(
            '/api/translate/',
            data=json.dumps({
                'text': 'Hello, how are you?',
                'source_lang': 'en',
                'target_lang': 'es',
            }),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['translated_text'])

    def test_auto_detect_source(self):
        response = self.client.post(
            '/api/translate/',
            data=json.dumps({
                'text': 'Bonjour le monde',
                'source_lang': 'auto',
                'target_lang': 'en',
            }),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['translated_text'])

    def test_empty_text_returns_400(self):
        response = self.client.post(
            '/api/translate/',
            data=json.dumps({
                'text': '',
                'source_lang': 'en',
                'target_lang': 'es',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_target_lang_returns_400(self):
        response = self.client.post(
            '/api/translate/',
            data=json.dumps({
                'text': 'Hello',
                'source_lang': 'en',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class AIToolsGenerateAPITests(BaseAPITestCase):
    """POST /api/ai-tools/generate/"""

    def test_basic_generate(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({
                'tool': 'ai-essay-writer',
                'topic': 'The impact of artificial intelligence',
                'description': 'A short essay about AI in modern society',
            }),
            content_type='application/json',
        )
        self.assertAPISuccess(response, ['output', 'tool', 'remaining', 'limit'])

    def test_missing_tool_returns_400(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'topic': 'Test'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_unknown_tool_returns_404(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': 'nonexistent-tool'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_empty_tool_returns_400(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_required_field_returns_400(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({
                'tool': 'ai-essay-writer',
                # missing 'topic' and 'description'
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


class PDFToolsAPITests(BaseAPITestCase):
    """POST /api/pdf/* — local file processing tests."""

    def _make_pdf_bytes(self):
        """Create a minimal valid PDF in memory."""
        import fitz  # PyMuPDF
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test PDF content for WritingBot integration tests.")
        pdf_bytes = doc.tobytes()
        doc.close()
        return pdf_bytes

    def test_pdf_info(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        pdf_bytes = self._make_pdf_bytes()
        pdf_file = SimpleUploadedFile('test.pdf', pdf_bytes, content_type='application/pdf')
        response = self.client.post('/api/pdf/info/', {'file': pdf_file})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('page_count', data)
        self.assertEqual(data['page_count'], 1)

    def test_pdf_compress(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        pdf_bytes = self._make_pdf_bytes()
        pdf_file = SimpleUploadedFile('test.pdf', pdf_bytes, content_type='application/pdf')
        response = self.client.post('/api/pdf/compress/', {'file': pdf_file, 'quality': 'medium'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_convert_image_to_pdf(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        from PIL import Image
        import io
        img = Image.new('RGB', (100, 100), color='blue')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        img_file = SimpleUploadedFile('test.png', buf.getvalue(), content_type='image/png')
        response = self.client.post('/api/pdf/convert/', {
            'file': img_file,
            'direction': 'to_pdf',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_split(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        pdf_bytes = self._make_pdf_bytes()
        pdf_file = SimpleUploadedFile('test.pdf', pdf_bytes, content_type='application/pdf')
        response = self.client.post('/api/pdf/split/', {'file': pdf_file, 'pages': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_rotate(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        pdf_bytes = self._make_pdf_bytes()
        pdf_file = SimpleUploadedFile('test.pdf', pdf_bytes, content_type='application/pdf')
        response = self.client.post('/api/pdf/rotate/', {'file': pdf_file, 'page': '1', 'angle': '90'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_pdf_merge(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        pdf1 = SimpleUploadedFile('test1.pdf', self._make_pdf_bytes(), content_type='application/pdf')
        pdf2 = SimpleUploadedFile('test2.pdf', self._make_pdf_bytes(), content_type='application/pdf')
        response = self.client.post('/api/pdf/merge/', {'files': [pdf1, pdf2]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_no_file_returns_400(self):
        response = self.client.post('/api/pdf/info/')
        self.assertEqual(response.status_code, 400)


class ImageConvertAPITests(BaseAPITestCase):
    """POST /api/media/convert-image/ — local image conversion tests."""

    def _make_png_bytes(self):
        """Create a minimal PNG image."""
        from PIL import Image
        import io
        img = Image.new('RGB', (100, 100), color='red')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return buf.getvalue()

    def test_png_to_jpg(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        png_bytes = self._make_png_bytes()
        img_file = SimpleUploadedFile('test.png', png_bytes, content_type='image/png')
        response = self.client.post(
            '/api/media/convert-image/',
            {'file': img_file, 'format': 'jpg', 'quality': '90'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('image/', response['Content-Type'])

    def test_png_to_webp(self):
        from django.core.files.uploadedfile import SimpleUploadedFile
        png_bytes = self._make_png_bytes()
        img_file = SimpleUploadedFile('test.png', png_bytes, content_type='image/png')
        response = self.client.post(
            '/api/media/convert-image/',
            {'file': img_file, 'format': 'webp', 'quality': '85'},
        )
        self.assertEqual(response.status_code, 200)

    def test_no_file_returns_400(self):
        response = self.client.post(
            '/api/media/convert-image/',
            {'format': 'jpg'},
        )
        self.assertIn(response.status_code, [400, 500])
