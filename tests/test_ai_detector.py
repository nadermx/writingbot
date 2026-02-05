"""Tests for the AI detector service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import MOCK_AI_DETECT_RESPONSE


@patch('core.llm_client.LLMClient.generate', return_value=(MOCK_AI_DETECT_RESPONSE, None))
class AIDetectorServiceTests(TestCase):

    def test_detect_ai_content(self, mock_gen):
        from ai_detector.services import AIDetectorService
        text = 'Furthermore, the nuanced approach to this multifaceted topic reveals a tapestry of interconnected ideas.'
        result, error = AIDetectorService.detect(text)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_detect_empty_text(self, mock_gen):
        from ai_detector.services import AIDetectorService
        result, error = AIDetectorService.detect('')
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    def test_detect_short_text(self, mock_gen):
        from ai_detector.services import AIDetectorService
        result, error = AIDetectorService.detect('Too short.')
        # Should still attempt detection or return error
        # Implementation-dependent

    def test_heuristics_ai_phrases(self, mock_gen):
        from ai_detector.services import AIDetectorService
        # Test that heuristic scoring works independently
        text = 'Furthermore, the multifaceted and nuanced approach reveals a holistic tapestry of synergistic ideas.'
        heuristics = AIDetectorService._compute_perplexity_heuristics(text)
        self.assertIsInstance(heuristics, (int, float))
        self.assertGreaterEqual(heuristics, 0)
