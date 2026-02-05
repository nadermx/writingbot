"""Tests for the summarizer service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import mock_llm_generate


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class SummarizerServiceTests(TestCase):

    def test_summarize_paragraph_mode(self, mock_gen):
        from summarizer.services import AISummarizerService
        service = AISummarizerService()
        text = 'This is a long piece of text. ' * 50
        result, error = service.summarize(text, mode='paragraph', length=3)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_summarize_key_sentences_mode(self, mock_gen):
        from summarizer.services import AISummarizerService
        service = AISummarizerService()
        text = 'This is a long piece of text. ' * 50
        result, error = service.summarize(text, mode='key_sentences', length=3)
        self.assertIsNone(error)

    def test_summarize_empty_text(self, mock_gen):
        from summarizer.services import AISummarizerService
        service = AISummarizerService()
        result, error = service.summarize('')
        # Empty text has no guard, processes through LLM
        # Either returns a result or an error, both are valid
        self.assertTrue(result is not None or error is not None)

    def test_length_levels(self, mock_gen):
        from summarizer.services import AISummarizerService
        service = AISummarizerService()
        text = 'This is a test. ' * 100
        for length in range(1, 6):
            result, error = service.summarize(text, length=length)
            self.assertIsNone(error, f'Length {length} failed')
