"""Tests for the grammar service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import MOCK_GRAMMAR_RESPONSE


@patch('core.llm_client.LLMClient.generate', return_value=(MOCK_GRAMMAR_RESPONSE, None))
class GrammarServiceTests(TestCase):

    def test_check_grammar(self, mock_gen):
        from grammar.services import AIGrammarService
        service = AIGrammarService()
        result, error = service.check_grammar('Teh cat sat on the mat.')
        self.assertIsNone(error)
        self.assertIsNotNone(result)
        self.assertIn('corrections', result)
        self.assertIn('writing_scores', result)

    def test_check_grammar_empty_text(self, mock_gen):
        from grammar.services import AIGrammarService
        service = AIGrammarService()
        result, error = service.check_grammar('')
        # Empty text still goes through LLM, returns result (no guard)
        self.assertIsInstance(result, (dict, type(None)))

    def test_fix_all(self, mock_gen):
        from grammar.services import AIGrammarService
        service = AIGrammarService()
        corrections = [
            {'original': 'teh', 'suggestion': 'the', 'position': {'start': 0, 'end': 3}},
        ]
        result, error = service.fix_all('teh cat', corrections)
        self.assertIsNone(error)
        self.assertEqual(result, 'the cat')

    def test_fix_single(self, mock_gen):
        from grammar.services import AIGrammarService
        service = AIGrammarService()
        correction = {'original': 'teh', 'suggestion': 'the', 'position': {'start': 0, 'end': 3}}
        result, error = service.fix_single('teh cat', correction)
        self.assertEqual(result, 'the cat')

    def test_premium_flag(self, mock_gen):
        from grammar.services import AIGrammarService
        service = AIGrammarService()
        service.check_grammar('Test text.', use_premium=True)
        call_kwargs = mock_gen.call_args[1]
        self.assertTrue(call_kwargs.get('use_premium', False))
