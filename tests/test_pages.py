"""
Test that all public page URLs return HTTP 200.
Catches template rendering errors, missing context, broken imports, etc.
"""
from django.test import TestCase, Client


class PublicPageTests(TestCase):
    """Test all public-facing pages return 200."""

    @classmethod
    def setUpTestData(cls):
        # Create the Language record needed by GlobalVars.get_globals()
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def _get(self, url, expected_status=200):
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, expected_status,
            f'{url} returned {response.status_code}, expected {expected_status}'
        )
        return response

    # ------------------------------------------------------------------
    # Core pages
    # ------------------------------------------------------------------
    def test_index(self):
        self._get('/')

    def test_login(self):
        self._get('/login/')

    def test_signup(self):
        self._get('/signup/')

    def test_lost_password(self):
        self._get('/lost-password/')

    def test_pricing(self):
        self._get('/pricing/')

    def test_contact(self):
        self._get('/contact/')

    def test_about(self):
        self._get('/about/')

    def test_terms(self):
        self._get('/terms/')

    def test_privacy(self):
        self._get('/privacy/')

    def test_refund(self):
        self._get('/refund/')

    def test_help(self):
        self._get('/help/')

    def test_trust_center(self):
        self._get('/trust-center/')

    def test_student_resources(self):
        self._get('/student-resources/')

    def test_professionals(self):
        self._get('/professionals/')

    # ------------------------------------------------------------------
    # Tool pages
    # ------------------------------------------------------------------
    def test_paraphraser(self):
        self._get('/paraphrasing-tool/')

    def test_grammar(self):
        self._get('/grammar-check/')

    def test_summarizer(self):
        self._get('/summarize/')

    def test_ai_detector(self):
        self._get('/ai-content-detector/')

    def test_humanizer(self):
        self._get('/ai-humanizer/')

    def test_plagiarism(self):
        self._get('/plagiarism-checker/')

    def test_translator(self):
        self._get('/translate/')

    def test_citations(self):
        self._get('/citation-generator/')

    def test_word_counter(self):
        self._get('/word-counter/')

    # ------------------------------------------------------------------
    # Flow (freemium, no login required)
    # ------------------------------------------------------------------
    def test_flow(self):
        self._get('/flow/')

    def test_ai_chat(self):
        self._get('/ai-chat/')

    def test_ai_search(self):
        self._get('/ai-search/')

    # ------------------------------------------------------------------
    # AI Tools
    # ------------------------------------------------------------------
    def test_ai_tools_index(self):
        self._get('/ai-writing-tools/')

    # ------------------------------------------------------------------
    # PDF Tools
    # ------------------------------------------------------------------
    def test_pdf_tools_index(self):
        self._get('/pdf-tools/')

    # ------------------------------------------------------------------
    # Media Tools
    # ------------------------------------------------------------------
    def test_image_tools(self):
        self._get('/image-tools/')

    def test_image_converter(self):
        self._get('/image-converter/')

    def test_background_remover(self):
        self._get('/background-remover/')

    def test_qr_code_generator(self):
        self._get('/tools/qr-code-generator/')

    def test_voice_generator(self):
        self._get('/tools/ai-voice-generator/')

    def test_transcription(self):
        self._get('/tools/transcription/')

    def test_logo_generator(self):
        self._get('/tools/logo-generator/')

    def test_character_generator(self):
        self._get('/tools/character-generator/')

    def test_word_cloud(self):
        self._get('/tools/word-cloud/')

    def test_banner_generator(self):
        self._get('/tools/banner-generator/')

    def test_presentation_maker(self):
        self._get('/tools/presentation-maker/')

    def test_media_tools_index(self):
        self._get('/media-tools/')

    # ------------------------------------------------------------------
    # SEO landing pages
    # ------------------------------------------------------------------
    def test_rewording_tool(self):
        self._get('/rewording-tool/')

    def test_sentence_rewriter(self):
        self._get('/sentence-rewriter/')

    def test_paragraph_rewriter(self):
        self._get('/paragraph-rewriter/')

    def test_essay_rewriter(self):
        self._get('/essay-rewriter/')

    def test_article_rewriter(self):
        self._get('/article-rewriter/')

    def test_text_rewriter(self):
        self._get('/text-rewriter/')

    def test_spell_checker(self):
        self._get('/spell-checker/')

    def test_punctuation_checker(self):
        self._get('/punctuation-checker/')

    def test_essay_checker(self):
        self._get('/essay-checker/')

    def test_online_proofreader(self):
        self._get('/online-proofreader/')

    # ------------------------------------------------------------------
    # Blog / Courses index
    # ------------------------------------------------------------------
    def test_blog_index(self):
        self._get('/blog/')

    def test_courses_index(self):
        self._get('/courses/')

    # ------------------------------------------------------------------
    # API docs
    # ------------------------------------------------------------------
    def test_api_docs(self):
        self._get('/api/docs/')


# ======================================================================
# Dynamic test classes — iterate registries to cover ALL pages
# ======================================================================

class AIToolPageTests(TestCase):
    """Test every AI writing tool page (98 generators) returns 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def test_all_ai_tool_pages(self):
        from ai_tools.generators.registry import GENERATOR_REGISTRY
        for slug in GENERATOR_REGISTRY:
            url = f'/ai-writing-tools/{slug}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'AI tool page {url} returned {response.status_code}'
            )


class PDFToolPageTests(TestCase):
    """Test every PDF tool page (16 tools) returns 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def test_all_pdf_tool_pages(self):
        from pdf_tools.views import PDF_TOOLS
        for tool in PDF_TOOLS:
            url = f'/pdf-tools/{tool["slug"]}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'PDF tool page {url} returned {response.status_code}'
            )


class MediaToolPageTests(TestCase):
    """Test every media/image tool page (27 tools) returns 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def test_all_media_tool_pages(self):
        from media_tools.views import IMAGE_TOOLS
        for slug in IMAGE_TOOLS:
            url = f'/tools/{slug}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Media tool page {url} returned {response.status_code}'
            )


class ConverterPairPageTests(TestCase):
    """Test a representative sample of converter pair pages returns 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    # Representative sample of image-to-image, doc-to-doc, and cross-type pairs
    SAMPLE_PAIRS = [
        # Image-to-image
        ('jpg', 'png'), ('png', 'webp'), ('webp', 'jpg'), ('gif', 'png'),
        ('bmp', 'jpg'), ('heic', 'jpg'), ('avif', 'png'), ('tiff', 'jpg'),
        # Document-to-document
        ('pdf', 'word'), ('word', 'pdf'), ('excel', 'csv'), ('csv', 'excel'),
        ('pdf', 'txt'), ('html', 'pdf'), ('odt', 'pdf'), ('rtf', 'pdf'),
        # Cross-type
        ('pdf', 'jpg'), ('pdf', 'png'), ('jpg', 'pdf'), ('png', 'pdf'),
    ]

    def test_converter_index(self):
        response = self.client.get('/convert/')
        self.assertEqual(response.status_code, 200)

    def test_sample_converter_pairs(self):
        for source, target in self.SAMPLE_PAIRS:
            url = f'/convert/{source}-to-{target}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Converter pair page {url} returned {response.status_code}'
            )


class TranslatorPageTests(TestCase):
    """Test translator language pages and pair pages return 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    SAMPLE_LANGUAGES = ['spanish', 'french', 'german', 'japanese', 'arabic']
    SAMPLE_PAIRS = [
        ('english', 'spanish'),
        ('english', 'french'),
        ('spanish', 'english'),
        ('french', 'german'),
        ('japanese', 'english'),
    ]

    def test_language_pages(self):
        for lang in self.SAMPLE_LANGUAGES:
            url = f'/translate/{lang}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Translator language page {url} returned {response.status_code}'
            )

    def test_pair_pages(self):
        for source, target in self.SAMPLE_PAIRS:
            url = f'/translate/{source}-to-{target}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Translator pair page {url} returned {response.status_code}'
            )


class SEOGrammarPageTests(TestCase):
    """Test all 10 language-specific grammar check SEO pages return 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    GRAMMAR_PAGES = [
        'german', 'french', 'spanish', 'portuguese', 'dutch',
        'italian', 'polish', 'swedish', 'russian', 'japanese',
    ]

    def test_all_grammar_seo_pages(self):
        for lang in self.GRAMMAR_PAGES:
            url = f'/{lang}-grammar-check/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Grammar SEO page {url} returned {response.status_code}'
            )


class GuidesPageTests(TestCase):
    """Test guides index + all 10 guide pages return 200."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    GUIDE_KEYS = [
        'paraphrasing', 'grammar', 'ai-writing-assistant',
        'apa-citation', 'mla-citation', 'chicago-citation',
        'academic-writing', 'business-writing', 'essay-writing',
        'plagiarism-prevention',
    ]

    def test_guides_index(self):
        response = self.client.get('/guides/')
        self.assertEqual(response.status_code, 200)

    def test_all_guide_pages(self):
        for key in self.GUIDE_KEYS:
            url = f'/guides/{key}/'
            response = self.client.get(url)
            self.assertEqual(
                response.status_code, 200,
                f'Guide page {url} returned {response.status_code}'
            )


class MiscPageTests(TestCase):
    """Test miscellaneous tool pages that aren't covered above."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()

    def test_proofreader(self):
        response = self.client.get('/proofreader/')
        self.assertEqual(response.status_code, 200)

    def test_character_counter(self):
        response = self.client.get('/character-counter/')
        self.assertEqual(response.status_code, 200)

    def test_text_case_converter(self):
        response = self.client.get('/text-case-converter/')
        self.assertEqual(response.status_code, 200)

    def test_speech_to_text(self):
        response = self.client.get('/speech-to-text/')
        self.assertEqual(response.status_code, 200)
