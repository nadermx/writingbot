"""
Tests for internal API POST endpoints with mocked LLM backend.
Covers paraphrase, grammar, summarize, AI detect, translate, and AI tools generate.
"""
import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client

from tests.conftest import (
    mock_llm_generate, MOCK_GRAMMAR_RESPONSE,
    MOCK_AI_DETECT_RESPONSE,
)


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
        # Clear DRF throttle caches so page tests don't cause 429s here
        from rest_framework.throttling import SimpleRateThrottle
        if hasattr(SimpleRateThrottle, 'cache'):
            SimpleRateThrottle.cache.clear()


def _grammar_aware_mock(system_prompt='', messages=None, max_tokens=4096,
                        temperature=0.7, use_premium=False):
    """Extended mock that also checks message content for grammar/detect keywords."""
    # Check messages for grammar/detect content when system_prompt is empty
    if not system_prompt and messages:
        msg_text = messages[0].get('content', '').lower() if messages else ''
        if 'grammar' in msg_text or 'corrections' in msg_text:
            return MOCK_GRAMMAR_RESPONSE, None
        if 'ai' in msg_text and ('written by' in msg_text or 'detect' in msg_text):
            return MOCK_AI_DETECT_RESPONSE, None
    return mock_llm_generate(system_prompt, messages, max_tokens, temperature, use_premium)


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class ParaphraseAPITests(BaseAPITestCase):
    """POST /api/paraphrase/"""

    def test_basic_paraphrase(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'The cat sat on the mat.', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('output_text', data)
        self.assertIsNotNone(data['output_text'])

    def test_empty_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': '', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_missing_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_mode_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'Hello world.', 'mode': 'nonexistent'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


@patch('core.llm_client.LLMClient.generate', side_effect=_grammar_aware_mock)
class GrammarCheckAPITests(BaseAPITestCase):
    """POST /api/grammar/check/"""

    def test_basic_grammar_check(self, mock_gen):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': 'Teh cat sat on teh mat.'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('corrections', data)
        self.assertIn('writing_scores', data)

    def test_empty_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_with_dialect(self, mock_gen):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': 'Colour is correct.', 'dialect': 'en-gb'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class SummarizeAPITests(BaseAPITestCase):
    """POST /api/summarize/"""

    def test_basic_summarize(self, mock_gen):
        long_text = 'This is a long article about technology. ' * 30
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': long_text}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        # Response should have summary-related fields
        self.assertTrue(
            'summary' in data or 'output_text' in data or 'key_points' in data,
            f'Unexpected summarize response keys: {list(data.keys())}'
        )

    def test_empty_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


@patch('core.llm_client.LLMClient.generate', side_effect=_grammar_aware_mock)
class AIDetectAPITests(BaseAPITestCase):
    """POST /api/ai-detect/"""

    def test_basic_detect(self, mock_gen):
        # AI detector requires at least 80 words
        text = ' '.join(['The quick brown fox jumps over the lazy dog.'] * 12)
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': text}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('classification', data)
        self.assertIn('overall_score', data)

    def test_empty_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_too_short_text_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': 'This is too short.'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class TranslateInternalAPITests(BaseAPITestCase):
    """POST /api/translate/ — uses external translateapi.ai, mock at service level."""

    def test_basic_translate(self):
        mock_result = {
            'translated_text': 'Hola, como estas?',
            'source_lang': 'en',
            'target_lang': 'es',
        }
        with patch('translator.services.TranslationService.translate', return_value=(mock_result, None)):
            response = self.client.post(
                '/api/translate/',
                data=json.dumps({
                    'text': 'Hello, how are you?',
                    'source_lang': 'en',
                    'target_lang': 'es',
                }),
                content_type='application/json',
            )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('translated_text', data)

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


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class AIToolsGenerateAPITests(BaseAPITestCase):
    """POST /api/ai-tools/generate/"""

    def test_basic_generate(self, mock_gen):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({
                'tool': 'ai-essay-writer',
                'topic': 'The impact of artificial intelligence',
                'description': 'A comprehensive essay about AI in modern society',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('output', data)

    def test_missing_tool_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'topic': 'Test'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_unknown_tool_returns_404(self, mock_gen):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': 'nonexistent-tool'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_empty_tool_returns_400(self, mock_gen):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_missing_required_field_returns_400(self, mock_gen):
        # ai-essay-writer requires 'topic' and 'description'
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({
                'tool': 'ai-essay-writer',
                # missing 'topic' and 'description'
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
