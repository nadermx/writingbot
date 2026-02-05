"""Tests for the paraphraser service."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import mock_llm_generate, MOCK_PARAPHRASE_RESPONSE, MOCK_SYNONYMS_RESPONSE


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class ParaphraseServiceTests(TestCase):

    def test_basic_paraphrase(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        text, error = AIParaphraseService.paraphrase('The cat sat on the mat.', mode='standard')
        self.assertIsNone(error)
        self.assertIsNotNone(text)

    def test_all_modes(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        for mode in AIParaphraseService.MODE_PROMPTS.keys():
            text, error = AIParaphraseService.paraphrase('Test text.', mode=mode)
            self.assertIsNone(error, f'Mode {mode} failed with error: {error}')

    def test_synonym_levels(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        for level in range(1, 6):
            text, error = AIParaphraseService.paraphrase('Test text.', synonym_level=level)
            self.assertIsNone(error, f'Synonym level {level} failed')

    def test_frozen_words(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        text, error = AIParaphraseService.paraphrase(
            'The WritingBot platform is great.',
            frozen_words=['WritingBot'],
        )
        self.assertIsNone(error)

    def test_custom_mode_with_instructions(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        text, error = AIParaphraseService.paraphrase(
            'Test text.',
            mode='custom',
            settings_dict={'custom_instructions': 'Make it funny'},
        )
        self.assertIsNone(error)

    def test_post_process_strips_quotes(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        result = AIParaphraseService._post_process('"Quoted text"', [], {})
        self.assertEqual(result, 'Quoted text')

    def test_word_count(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        self.assertEqual(AIParaphraseService.count_words('one two three'), 3)
        self.assertEqual(AIParaphraseService.count_words(''), 0)
        self.assertEqual(AIParaphraseService.count_words(None), 0)

    def test_get_synonyms(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        synonyms, error = AIParaphraseService.get_synonyms('fast', 'The car was fast.')
        self.assertIsNone(error)
        self.assertIsInstance(synonyms, list)

    def test_premium_flag_passed(self, mock_gen):
        from paraphraser.services import AIParaphraseService
        AIParaphraseService.paraphrase('Test text.', use_premium=True)
        # Check that the mock was called with use_premium=True
        call_kwargs = mock_gen.call_args[1]
        self.assertTrue(call_kwargs.get('use_premium', False))
