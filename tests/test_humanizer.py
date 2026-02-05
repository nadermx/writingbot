"""Tests for the humanizer service."""
from unittest.mock import patch, call

from django.test import TestCase

from tests.conftest import MOCK_HUMANIZE_SCORE_RESPONSE, MOCK_HUMANIZE_TEXT_RESPONSE


class HumanizerServiceTests(TestCase):

    @patch('core.llm_client.LLMClient.generate')
    def test_humanize_basic(self, mock_gen):
        from humanizer.services import AIHumanizerService
        # Three calls: score before, rewrite, score after
        mock_gen.side_effect = [
            (MOCK_HUMANIZE_SCORE_RESPONSE, None),  # AI score before
            (MOCK_HUMANIZE_TEXT_RESPONSE, None),     # Rewrite
            ('15', None),                             # AI score after
        ]
        result, error = AIHumanizerService.humanize('AI-generated text here.', mode='basic')
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn('output_text', result)
        self.assertEqual(mock_gen.call_count, 3)

    @patch('core.llm_client.LLMClient.generate')
    def test_humanize_advanced(self, mock_gen):
        from humanizer.services import AIHumanizerService
        mock_gen.side_effect = [
            ('80', None),
            (MOCK_HUMANIZE_TEXT_RESPONSE, None),
            ('10', None),
        ]
        result, error = AIHumanizerService.humanize('AI-generated text here.', mode='advanced')
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    @patch('core.llm_client.LLMClient.generate')
    def test_humanize_empty_text(self, mock_gen):
        from humanizer.services import AIHumanizerService
        result, error = AIHumanizerService.humanize('')
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    @patch('core.llm_client.LLMClient.generate')
    def test_humanize_error_handling(self, mock_gen):
        from humanizer.services import AIHumanizerService
        mock_gen.return_value = (None, 'LLM service error')
        result, error = AIHumanizerService.humanize('Test text.')
        self.assertIsNone(result)
        self.assertIsNotNone(error)
