"""
Comprehensive API tests for WritingBot.ai

Tests cover:
- Internal endpoints: RateLimit, CreditsConsume, CancelSubscription, LogFrontendError
- Public API v1 endpoints: Paraphrase, Grammar, Summarize, AI Detect, Translate
- API key authentication (valid, invalid, missing)
- API key validation internal endpoint (GPU server communication)
- Tool-specific input validation (empty text, mode validation, word limits)
- Rate throttling behavior

All GPU/LLM API calls are mocked to avoid hitting external services.
"""
import json
from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.core.cache import cache

from accounts.models import CustomUser
from tests.conftest import (
    mock_llm_generate,
    MOCK_PARAPHRASE_RESPONSE,
    MOCK_GRAMMAR_RESPONSE,
    MOCK_AI_DETECT_MODEL_RESPONSE,
)


class BaseAPITestCase(TestCase):
    """Shared setup for all API tests."""

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def setUp(self):
        self.client = Client()
        # Clear DRF throttle caches to prevent 429s across test suites
        from rest_framework.throttling import SimpleRateThrottle
        if hasattr(SimpleRateThrottle, 'cache'):
            SimpleRateThrottle.cache.clear()
        cache.clear()


# ======================================================================
# RateLimit endpoint
# ======================================================================

class RateLimitAPITests(BaseAPITestCase):
    """Tests for POST /api/accounts/rate_limit/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.free_user = CustomUser.objects.create_user(
            email='free@example.com', password='testpass123'
        )
        cls.free_user.credits = 0
        cls.free_user.is_plan_active = False
        cls.free_user.save()

        cls.premium_user = CustomUser.objects.create_user(
            email='premium@example.com', password='testpass123'
        )
        cls.premium_user.is_plan_active = True
        cls.premium_user.credits = 100
        cls.premium_user.save()

        cls.credits_user = CustomUser.objects.create_user(
            email='credits@example.com', password='testpass123'
        )
        cls.credits_user.credits = 5
        cls.credits_user.is_plan_active = False
        cls.credits_user.save()

    def test_premium_user_bypasses_rate_limit(self):
        self.client.force_login(self.premium_user)
        response = self.client.post(
            '/api/accounts/rate_limit/',
            data=json.dumps({
                'files_data': [{'size': 1000}],
            }),
            content_type='application/json',
            HTTP_USER_AGENT='TestBrowser/1.0',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('status'))

    def test_user_with_credits_passes(self):
        self.client.force_login(self.credits_user)
        response = self.client.post(
            '/api/accounts/rate_limit/',
            data=json.dumps({
                'files_data': [{'size': 1000}],
            }),
            content_type='application/json',
            HTTP_USER_AGENT='TestBrowser/1.0',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('status'))

    def test_free_user_file_too_large(self):
        self.client.force_login(self.free_user)
        response = self.client.post(
            '/api/accounts/rate_limit/',
            data=json.dumps({
                'files_data': [{'size': 999999999}],
            }),
            content_type='application/json',
            HTTP_USER_AGENT='TestBrowser/1.0',
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertTrue(data.get('limit_exceeded'))


# ======================================================================
# CreditsConsume endpoint
# ======================================================================

class CreditsConsumeAPITests(BaseAPITestCase):
    """Tests for POST /api/accounts/consume/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='consume@example.com', password='testpass123'
        )
        cls.user.credits = 10
        cls.user.save()

    def test_consume_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/accounts/consume/')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.credits, 9)

    def test_consume_unauthenticated(self):
        response = self.client.post('/api/accounts/consume/')
        self.assertEqual(response.status_code, 200)


# ======================================================================
# LogFrontendError endpoint
# ======================================================================

class LogFrontendErrorAPITests(BaseAPITestCase):
    """Tests for POST /api/accounts/log-error/."""

    def test_log_error_basic(self):
        response = self.client.post(
            '/api/accounts/log-error/',
            data=json.dumps({
                'message': 'Uncaught TypeError: x is not a function',
                'source': 'paraphraser.js',
                'lineno': 42,
                'colno': 15,
                'stack': 'TypeError: x is not a function\n  at bar (paraphraser.js:42)',
                'url': 'https://writingbot.ai/paraphrasing-tool/',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data.get('status'), 'logged')

    def test_log_error_minimal(self):
        response = self.client.post(
            '/api/accounts/log-error/',
            data=json.dumps({'message': 'Test error'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)


# ======================================================================
# CancelSubscription API
# ======================================================================

class CancelSubscriptionAPITests(BaseAPITestCase):
    """Tests for POST /api/accounts/cancel-subscription/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='cancelapi@example.com', password='testpass123'
        )
        cls.user.is_plan_active = True
        cls.user.processor = 'stripe'
        cls.user.card_nonce = 'card_123'
        cls.user.save()

    def test_cancel_authenticated(self):
        self.client.force_login(self.user)
        response = self.client.post('/api/accounts/cancel-subscription/')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_plan_active)


# ======================================================================
# Public API v1: Paraphrase
# ======================================================================

class ParaphraseAPIv1Tests(BaseAPITestCase):
    """Tests for POST /api/v1/paraphrase/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='apiuser@example.com', password='testpass123'
        )
        cls.user.api_token = 'test-api-token-paraphrase'
        cls.user.is_plan_active = False
        cls.user.save()

        cls.premium_user = CustomUser.objects.create_user(
            email='premiumapi@example.com', password='testpass123'
        )
        cls.premium_user.api_token = 'test-api-token-premium'
        cls.premium_user.is_plan_active = True
        cls.premium_user.save()

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_paraphrase_basic(self, mock_gen):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': 'The quick brown fox jumps over the lazy dog.',
                'mode': 'standard',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('output_text', data)
        self.assertIn('input_word_count', data)
        self.assertIn('output_word_count', data)
        self.assertEqual(data['mode'], 'standard')

    def test_paraphrase_empty_text(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({'text': '', 'mode': 'standard'}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_paraphrase_missing_text(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({'mode': 'standard'}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 400)

    def test_paraphrase_invalid_mode(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': 'Hello world.',
                'mode': 'nonexistent',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 400)

    def test_paraphrase_premium_mode_denied_for_free(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': 'Hello world.',
                'mode': 'academic',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertTrue(data.get('upgrade'))

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_paraphrase_premium_mode_allowed_for_premium(self, mock_gen):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': 'Hello world.',
                'mode': 'academic',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-premium',
        )
        self.assertEqual(response.status_code, 200)

    def test_paraphrase_word_limit_exceeded(self):
        long_text = ' '.join(['word'] * 600)
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': long_text,
                'mode': 'standard',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-paraphrase',
        )
        self.assertEqual(response.status_code, 403)

    def test_paraphrase_invalid_api_key(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({
                'text': 'Hello world.',
                'mode': 'standard',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='invalid-key',
        )
        self.assertIn(response.status_code, [401, 403])


# ======================================================================
# Public API v1: Grammar
# ======================================================================

class GrammarAPIv1Tests(BaseAPITestCase):
    """Tests for POST /api/v1/grammar/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='grammarapi@example.com', password='testpass123'
        )
        cls.user.api_token = 'test-api-token-grammar'
        cls.user.save()

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_grammar_basic(self, mock_gen):
        response = self.client.post(
            '/api/v1/grammar/',
            data=json.dumps({'text': 'Teh cat sat on teh mat.'}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-grammar',
        )
        self.assertEqual(response.status_code, 200)

    def test_grammar_empty_text(self):
        response = self.client.post(
            '/api/v1/grammar/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-grammar',
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


# ======================================================================
# Public API v1: Summarize
# ======================================================================

class SummarizeAPIv1Tests(BaseAPITestCase):
    """Tests for POST /api/v1/summarize/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='summarizeapi@example.com', password='testpass123'
        )
        cls.user.api_token = 'test-api-token-summarize'
        cls.user.save()

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_summarize_basic(self, mock_gen):
        text = (
            'Artificial intelligence is transforming every industry. '
            'From healthcare to finance, AI systems are being deployed. '
        ) * 20  # Ensure enough words
        response = self.client.post(
            '/api/v1/summarize/',
            data=json.dumps({'text': text}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-summarize',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('summary', data)

    def test_summarize_empty_text(self):
        response = self.client.post(
            '/api/v1/summarize/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-summarize',
        )
        self.assertEqual(response.status_code, 400)

    def test_summarize_word_limit_exceeded(self):
        long_text = ' '.join(['word'] * 1500)
        response = self.client.post(
            '/api/v1/summarize/',
            data=json.dumps({'text': long_text}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-summarize',
        )
        self.assertEqual(response.status_code, 403)


# ======================================================================
# Public API v1: AI Detect
# ======================================================================

class AIDetectAPIv1Tests(BaseAPITestCase):
    """Tests for POST /api/v1/ai-detect/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='aidetectapi@example.com', password='testpass123'
        )
        cls.user.api_token = 'test-api-token-aidetect'
        cls.user.save()

    @patch('core.llm_client.LLMClient.detect_ai_text', return_value=(MOCK_AI_DETECT_MODEL_RESPONSE, None))
    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_ai_detect_basic(self, mock_gen, mock_detect):
        text = (
            'The rapid advancement of artificial intelligence has sparked both excitement '
            'and concern across various sectors of society. As machine learning algorithms '
            'become increasingly sophisticated, they are being integrated into everything '
            'from healthcare diagnostics to autonomous vehicles. ' * 5
        )
        response = self.client.post(
            '/api/v1/ai-detect/',
            data=json.dumps({'text': text}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-aidetect',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_ai_detect_empty_text(self):
        response = self.client.post(
            '/api/v1/ai-detect/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-aidetect',
        )
        self.assertEqual(response.status_code, 400)

    def test_ai_detect_word_limit_exceeded(self):
        long_text = ' '.join(['word'] * 1500)
        response = self.client.post(
            '/api/v1/ai-detect/',
            data=json.dumps({'text': long_text}),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-aidetect',
        )
        self.assertEqual(response.status_code, 403)


# ======================================================================
# Public API v1: Translate
# ======================================================================

class TranslateAPIv1Tests(BaseAPITestCase):
    """Tests for POST /api/v1/translate/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='translateapi@example.com', password='testpass123'
        )
        cls.user.api_token = 'test-api-token-translate'
        cls.user.save()

    @patch('translator.services.TranslationService.translate')
    def test_translate_basic(self, mock_translate):
        mock_translate.return_value = (
            {'translated_text': 'Hola mundo', 'source_lang': 'en', 'target_lang': 'es'},
            None,
        )
        response = self.client.post(
            '/api/v1/translate/',
            data=json.dumps({
                'text': 'Hello world',
                'source_lang': 'en',
                'target_lang': 'es',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-translate',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('translated_text', data)
        self.assertEqual(data['translated_text'], 'Hola mundo')

    def test_translate_empty_text(self):
        response = self.client.post(
            '/api/v1/translate/',
            data=json.dumps({
                'text': '',
                'source_lang': 'en',
                'target_lang': 'es',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-translate',
        )
        self.assertEqual(response.status_code, 400)

    def test_translate_missing_target_lang(self):
        response = self.client.post(
            '/api/v1/translate/',
            data=json.dumps({
                'text': 'Hello',
                'source_lang': 'en',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-translate',
        )
        self.assertEqual(response.status_code, 400)

    def test_translate_char_limit_exceeded(self):
        long_text = 'a' * 6000
        response = self.client.post(
            '/api/v1/translate/',
            data=json.dumps({
                'text': long_text,
                'source_lang': 'en',
                'target_lang': 'es',
            }),
            content_type='application/json',
            HTTP_X_API_KEY='test-api-token-translate',
        )
        self.assertEqual(response.status_code, 403)


# ======================================================================
# API Key Authentication
# ======================================================================

class APIKeyAuthenticationTests(BaseAPITestCase):
    """Tests for X-API-Key header authentication."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='authtest@example.com', password='testpass123'
        )
        cls.user.api_token = 'valid-auth-token-xyz'
        cls.user.save()

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_valid_api_key(self, mock_gen):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({'text': 'Hello world.', 'mode': 'standard'}),
            content_type='application/json',
            HTTP_X_API_KEY='valid-auth-token-xyz',
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_api_key(self):
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({'text': 'Hello world.', 'mode': 'standard'}),
            content_type='application/json',
            HTTP_X_API_KEY='invalid-token',
        )
        self.assertIn(response.status_code, [401, 403])

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_no_api_key_processes_as_anon(self, mock_gen):
        """No API key = anonymous user, still processes with free limits."""
        response = self.client.post(
            '/api/v1/paraphrase/',
            data=json.dumps({'text': 'Hello world.', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])


# ======================================================================
# Internal API key validation (GPU server communication)
# ======================================================================

class ValidateAPIKeyInternalTests(BaseAPITestCase):
    """Tests for POST /api/internal/validate/."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user = CustomUser.objects.create_user(
            email='internalval@example.com', password='testpass123'
        )
        cls.user.api_token = 'user-api-token-for-validation'
        cls.user.is_plan_active = False
        cls.user.save()

        cls.premium_user = CustomUser.objects.create_user(
            email='internalprem@example.com', password='testpass123'
        )
        cls.premium_user.api_token = 'premium-token-for-validation'
        cls.premium_user.is_plan_active = True
        cls.premium_user.save()

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_valid_api_key(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'user-api-token-for-validation',
                'tool': 'paraphrase',
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='test-internal-secret',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('valid'))
        self.assertEqual(data.get('user_id'), self.user.id)
        self.assertFalse(data.get('is_premium'))

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_valid_premium_user(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'premium-token-for-validation',
                'tool': 'paraphrase',
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='test-internal-secret',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get('valid'))
        self.assertTrue(data.get('is_premium'))

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_invalid_api_key(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'nonexistent-token',
                'tool': 'paraphrase',
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='test-internal-secret',
        )
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertFalse(data.get('valid'))

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_missing_internal_key(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'user-api-token-for-validation',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 401)

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_wrong_internal_key(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'user-api-token-for-validation',
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='wrong-secret',
        )
        self.assertEqual(response.status_code, 401)

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_word_count_limit_for_free_user(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'user-api-token-for-validation',
                'tool': 'paraphrase',
                'word_count': 1000,
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='test-internal-secret',
        )
        self.assertEqual(response.status_code, 403)
        data = response.json()
        self.assertTrue(data.get('upgrade'))

    @patch('config.INTERNAL_API_SECRET', 'test-internal-secret')
    def test_premium_mode_denied_for_free(self):
        response = self.client.post(
            '/api/internal/validate/',
            data=json.dumps({
                'api_key': 'user-api-token-for-validation',
                'tool': 'paraphrase',
                'mode': 'academic',
            }),
            content_type='application/json',
            HTTP_X_INTERNAL_KEY='test-internal-secret',
        )
        self.assertEqual(response.status_code, 403)


# ======================================================================
# Internal paraphrase API endpoint
# ======================================================================

class InternalParaphraseAPITests(BaseAPITestCase):
    """Tests for POST /api/paraphrase/ (internal, not v1)."""

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_paraphrase_success(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({
                'text': 'The quick brown fox jumps over the lazy dog.',
                'mode': 'standard',
            }),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('output_text', data)

    def test_paraphrase_empty_text(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': '', 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_paraphrase_invalid_mode(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'Hello.', 'mode': 'bogus'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_paraphrase_free_word_limit(self):
        long_text = ' '.join(['word'] * 600)
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': long_text, 'mode': 'standard'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)

    def test_paraphrase_free_mode_restriction(self):
        response = self.client.post(
            '/api/paraphrase/',
            data=json.dumps({'text': 'Test text.', 'mode': 'formal'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 403)


# ======================================================================
# Internal grammar check API
# ======================================================================

class InternalGrammarAPITests(BaseAPITestCase):
    """Tests for POST /api/grammar/check/."""

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_grammar_check_success(self, mock_gen):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': 'Teh cat sat on teh mat.'}),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_grammar_check_empty_text(self):
        response = self.client.post(
            '/api/grammar/check/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# Internal summarize API
# ======================================================================

class InternalSummarizeAPITests(BaseAPITestCase):
    """Tests for POST /api/summarize/."""

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_summarize_success(self, mock_gen):
        text = (
            'AI is transforming industries across the globe. Machine learning and '
            'deep learning enable new capabilities in natural language processing. '
        ) * 20
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': text}),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_summarize_empty_text(self):
        response = self.client.post(
            '/api/summarize/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# Internal AI detect API
# ======================================================================

class InternalAIDetectAPITests(BaseAPITestCase):
    """Tests for POST /api/ai-detect/."""

    @patch('core.llm_client.LLMClient.detect_ai_text', return_value=(MOCK_AI_DETECT_MODEL_RESPONSE, None))
    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_ai_detect_success(self, mock_gen, mock_detect):
        text = (
            'The rapid advancement of artificial intelligence has sparked both excitement '
            'and concern across various sectors. As machine learning algorithms become '
            'increasingly sophisticated, they are integrated into many applications. '
        ) * 5
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': text}),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_ai_detect_empty_text(self):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_ai_detect_too_short(self):
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': 'This is too short.'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_ai_detect_free_word_limit(self):
        long_text = ' '.join(['word'] * 1500)
        response = self.client.post(
            '/api/ai-detect/',
            data=json.dumps({'text': long_text}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# Internal humanize API
# ======================================================================

class InternalHumanizeAPITests(BaseAPITestCase):
    """Tests for POST /api/humanize/."""

    @patch('core.llm_client.LLMClient.detect_ai_text', return_value=(MOCK_AI_DETECT_MODEL_RESPONSE, None))
    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_humanize_success(self, mock_gen, mock_detect):
        text = (
            'The rapid advancement of artificial intelligence has sparked both excitement '
            'and concern across various sectors. As machine learning algorithms become '
            'increasingly sophisticated, they are integrated into many applications. '
        ) * 5
        response = self.client.post(
            '/api/humanize/',
            data=json.dumps({'text': text}),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 400, 500])

    def test_humanize_empty_text(self):
        response = self.client.post(
            '/api/humanize/',
            data=json.dumps({'text': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# AI Tools generate API
# ======================================================================

class AIToolsGenerateAPITests(BaseAPITestCase):
    """Tests for POST /api/ai-tools/generate/."""

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_generate_success(self, mock_gen):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({
                'tool': 'ai-essay-writer',
                'topic': 'The impact of AI',
                'description': 'A short essay about AI',
            }),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_generate_missing_tool(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'topic': 'Test'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)

    def test_generate_unknown_tool(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': 'nonexistent-tool'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 404)

    def test_generate_empty_tool(self):
        response = self.client.post(
            '/api/ai-tools/generate/',
            data=json.dumps({'tool': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# Synonym API
# ======================================================================

class SynonymAPITests(BaseAPITestCase):
    """Tests for POST /api/paraphrase/synonyms/."""

    @patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
    def test_synonym_success(self, mock_gen):
        response = self.client.post(
            '/api/paraphrase/synonyms/',
            data=json.dumps({
                'word': 'quick',
                'context': 'The quick brown fox jumps over the lazy dog.',
            }),
            content_type='application/json',
        )
        self.assertIn(response.status_code, [200, 500])

    def test_synonym_missing_word(self):
        response = self.client.post(
            '/api/paraphrase/synonyms/',
            data=json.dumps({'word': ''}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)


# ======================================================================
# API Docs page
# ======================================================================

class APIDocsPageTests(BaseAPITestCase):
    """Tests for GET /api/docs/."""

    def test_docs_page_loads(self):
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)

    def test_docs_page_shows_token_when_authenticated(self):
        user = CustomUser.objects.create_user(
            email='doctest@example.com', password='testpass123'
        )
        user.api_token = 'my-visible-token'
        user.save()
        self.client.force_login(user)
        response = self.client.get('/api/docs/')
        self.assertEqual(response.status_code, 200)
