"""Tests for core.llm_client.LLMClient."""
from unittest.mock import patch, MagicMock

from django.test import TestCase, override_settings


class LLMClientTestCase(TestCase):
    """Test LLMClient routing and error handling."""

    @patch('core.llm_client.requests.post')
    def test_open_source_call_success(self, mock_post):
        """Test successful open-source LLM call."""
        from core.llm_client import LLMClient

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            'text': 'Generated text here.',
            'model': 'mistral-7b',
            'tokens_used': 50,
        }
        mock_post.return_value = mock_resp

        with self.settings(WRITINGBOT_API_URL='https://api.test.com', WRITINGBOT_API_KEY='test-key'):
            text, error = LLMClient.generate(
                system_prompt='You are a helper.',
                messages=[{'role': 'user', 'content': 'Hello'}],
            )

        self.assertEqual(text, 'Generated text here.')
        self.assertIsNone(error)
        mock_post.assert_called_once()

    @patch('core.llm_client.requests.post')
    def test_open_source_call_error(self, mock_post):
        """Test open-source LLM call with server error."""
        from core.llm_client import LLMClient

        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.headers = {'content-type': 'application/json'}
        mock_resp.json.return_value = {'error': 'Internal server error'}
        mock_post.return_value = mock_resp

        with self.settings(WRITINGBOT_API_URL='https://api.test.com', WRITINGBOT_API_KEY='test-key'):
            text, error = LLMClient.generate(
                system_prompt='You are a helper.',
                messages=[{'role': 'user', 'content': 'Hello'}],
            )

        self.assertIsNone(text)
        self.assertIsNotNone(error)

    @patch('core.llm_client.requests.post')
    def test_open_source_call_timeout(self, mock_post):
        """Test open-source LLM call timeout."""
        import requests as req
        from core.llm_client import LLMClient

        mock_post.side_effect = req.exceptions.Timeout()

        with self.settings(WRITINGBOT_API_URL='https://api.test.com', WRITINGBOT_API_KEY='test-key'):
            text, error = LLMClient.generate(
                system_prompt='You are a helper.',
                messages=[{'role': 'user', 'content': 'Hello'}],
            )

        self.assertIsNone(text)
        self.assertIn('timed out', error.lower())

    def test_no_api_url_configured(self):
        """Test error when no API URL is configured."""
        from core.llm_client import LLMClient

        with self.settings(WRITINGBOT_API_URL='', WRITINGBOT_API_KEY=''):
            text, error = LLMClient.generate(
                system_prompt='You are a helper.',
                messages=[{'role': 'user', 'content': 'Hello'}],
            )

        self.assertIsNone(text)
        self.assertIn('not configured', error.lower())

    @patch('core.llm_client.requests.post')
    def test_premium_routes_to_claude(self, mock_post):
        """Test that use_premium=True routes to Claude when API key is set."""
        from core.llm_client import LLMClient

        with patch.object(LLMClient, '_call_claude', return_value=('Claude response', None)) as mock_claude:
            with self.settings(ANTHROPIC_API_KEY='test-key'):
                text, error = LLMClient.generate(
                    system_prompt='Test',
                    messages=[{'role': 'user', 'content': 'Hello'}],
                    use_premium=True,
                )

        mock_claude.assert_called_once()
        mock_post.assert_not_called()
        self.assertEqual(text, 'Claude response')

    @patch('core.llm_client.requests.post')
    def test_premium_falls_back_to_open_source(self, mock_post):
        """Test that use_premium=True falls back to open-source when no Claude key."""
        from core.llm_client import LLMClient

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'text': 'OS response', 'model': 'mistral-7b', 'tokens_used': 10}
        mock_post.return_value = mock_resp

        with self.settings(ANTHROPIC_API_KEY='', WRITINGBOT_API_URL='https://api.test.com', WRITINGBOT_API_KEY='k'):
            text, error = LLMClient.generate(
                system_prompt='Test',
                messages=[{'role': 'user', 'content': 'Hello'}],
                use_premium=True,
            )

        mock_post.assert_called_once()
        self.assertEqual(text, 'OS response')
