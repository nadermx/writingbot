"""Tests for the Flow co-writer service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import (
    mock_llm_generate, MOCK_REVIEW_RESPONSE, MOCK_OUTLINE_RESPONSE,
    MOCK_OUTLINE_JSON_RESPONSE, MOCK_CHAT_RESPONSE, MOCK_SEARCH_RESPONSE,
)


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class FlowServiceTests(TestCase):

    def test_suggest_next(self, mock_gen):
        from flow.services import FlowService
        suggestion, error = FlowService.suggest_next('The sun was shining brightly.')
        self.assertIsNone(error)
        self.assertIsNotNone(suggestion)

    def test_suggest_next_empty_text(self, mock_gen):
        from flow.services import FlowService
        suggestion, error = FlowService.suggest_next('')
        self.assertIsNone(error)
        self.assertEqual(suggestion, 'Start writing your document here...')

    def test_suggest_next_with_cursor(self, mock_gen):
        from flow.services import FlowService
        text = 'The cat sat on the mat.'
        suggestion, error = FlowService.suggest_next(text, cursor_position=10)
        self.assertIsNone(error)

    def test_ai_review(self, mock_gen):
        from flow.services import FlowService
        review, error = FlowService.ai_review('This is a well-written document about testing.')
        self.assertIsNone(error)
        self.assertIsNotNone(review)

    def test_ai_review_empty(self, mock_gen):
        from flow.services import FlowService
        review, error = FlowService.ai_review('')
        self.assertIsNone(review)
        self.assertIsNotNone(error)

    def test_smart_start(self, mock_gen):
        from flow.services import FlowService
        outline, error = FlowService.smart_start('artificial intelligence in education')
        self.assertIsNone(error)
        self.assertIsNotNone(outline)

    def test_smart_start_empty(self, mock_gen):
        from flow.services import FlowService
        outline, error = FlowService.smart_start('')
        self.assertIsNone(outline)
        self.assertIsNotNone(error)

    def test_generate_outline(self, mock_gen):
        from flow.services import FlowService
        outline, error = FlowService.generate_outline('climate change')
        self.assertIsNone(error)

    def test_chat(self, mock_gen):
        from flow.services import FlowService
        reply, error = FlowService.chat('How do I improve my essay?')
        self.assertIsNone(error)
        self.assertIsNotNone(reply)

    def test_chat_with_history(self, mock_gen):
        from flow.services import FlowService
        history = [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'},
        ]
        reply, error = FlowService.chat('How do I write better?', history=history)
        self.assertIsNone(error)

    def test_chat_empty_message(self, mock_gen):
        from flow.services import FlowService
        reply, error = FlowService.chat('')
        self.assertIsNone(reply)
        self.assertIsNotNone(error)

    def test_search(self, mock_gen):
        from flow.services import FlowService
        result, error = FlowService.search('best practices for writing essays')
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn('answer', result)
        self.assertIn('sources', result)

    def test_search_empty_query(self, mock_gen):
        from flow.services import FlowService
        result, error = FlowService.search('')
        self.assertIsNone(result)
        self.assertIsNotNone(error)


class FlowResearchSearchTests(TestCase):
    """Test the DuckDuckGo-based research_search (no LLM mock needed)."""

    @patch('flow.services.requests.get')
    def test_research_search_success(self, mock_get):
        from flow.services import FlowService

        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '''
        <a class="result__a" href="https://example.com">Test Title</a>
        <a class="result__snippet">This is a test snippet.</a>
        '''
        results, error = FlowService.research_search('test query')
        self.assertIsNone(error)
        self.assertIsInstance(results, list)

    def test_research_search_empty_query(self):
        from flow.services import FlowService
        results, error = FlowService.research_search('')
        self.assertIsNone(results)
        self.assertIsNotNone(error)

    @patch('flow.services.requests.get')
    def test_research_search_timeout(self, mock_get):
        import requests as req
        from flow.services import FlowService
        mock_get.side_effect = req.exceptions.Timeout()
        results, error = FlowService.research_search('test')
        self.assertIsNone(results)
        self.assertIn('timed out', error.lower())


class FlowRateLimitTests(TestCase):
    """Test rate limiting helpers."""

    def test_ip_hash(self):
        from flow.services import FlowService
        h1 = FlowService._ip_hash('1.2.3.4', 'Mozilla')
        h2 = FlowService._ip_hash('1.2.3.4', 'Mozilla')
        h3 = FlowService._ip_hash('5.6.7.8', 'Mozilla')
        self.assertEqual(h1, h2)
        self.assertNotEqual(h1, h3)
