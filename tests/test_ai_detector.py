"""Tests for the AI detector service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import MOCK_AI_DETECT_MODEL_RESPONSE


@patch('core.llm_client.LLMClient.detect_ai_text', return_value=(MOCK_AI_DETECT_MODEL_RESPONSE, None))
class AIDetectorServiceTests(TestCase):

    def test_detect_ai_content(self, mock_detect):
        from ai_detector.services import AIDetectorService
        text = 'Furthermore, the nuanced approach to this multifaceted topic reveals a tapestry of interconnected ideas.'
        result, error = AIDetectorService.detect(text)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn('overall_score', result)
        self.assertIn('classification', result)
        self.assertIn('category_confidences', result)
        self.assertIn('sentences', result)
        mock_detect.assert_called_once()

    def test_detect_empty_text(self, mock_detect):
        from ai_detector.services import AIDetectorService
        result, error = AIDetectorService.detect('')
        self.assertIsNone(result)
        self.assertIsNotNone(error)

    def test_detect_short_text(self, mock_detect):
        from ai_detector.services import AIDetectorService
        result, error = AIDetectorService.detect('Too short.')
        # Should still attempt detection (model handles short text)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_heuristics_ai_phrases(self, mock_detect):
        from ai_detector.services import AIDetectorService
        # Test that heuristic scoring works independently
        text = 'Furthermore, the multifaceted and nuanced approach reveals a holistic tapestry of synergistic ideas.'
        heuristics = AIDetectorService._compute_perplexity_heuristics(text)
        self.assertIsInstance(heuristics, (int, float))
        self.assertGreaterEqual(heuristics, 0)

    def test_detect_fallback_on_model_error(self, mock_detect):
        """When GPU model is unavailable, fall back to heuristics-only."""
        from ai_detector.services import AIDetectorService
        mock_detect.return_value = (None, 'Service unavailable')
        text = 'Furthermore, the nuanced approach to this multifaceted topic reveals a tapestry of interconnected ideas.'
        result, error = AIDetectorService.detect(text)
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn('overall_score', result)

    def test_score_to_confidences(self, mock_detect):
        from ai_detector.services import AIDetectorService
        # High score -> ai_generated dominant
        confs = AIDetectorService._score_to_confidences(90)
        self.assertEqual(max(confs, key=confs.get), 'ai_generated')
        # Low score -> human_written dominant
        confs = AIDetectorService._score_to_confidences(10)
        self.assertEqual(max(confs, key=confs.get), 'human_written')
