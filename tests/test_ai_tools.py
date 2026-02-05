"""Tests for the AI tools generator framework."""
from unittest.mock import patch

from django.test import TestCase

from tests.conftest import mock_llm_generate


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class BaseGeneratorTests(TestCase):

    def test_base_generate(self, mock_gen):
        from ai_tools.generators.base import BaseGenerator
        gen = BaseGenerator()
        gen.slug = 'test'
        gen.system_prompt = 'You are a {tone} writer.'
        gen.fields = [{'name': 'topic', 'label': 'Topic'}]
        text, error = gen.generate({'topic': 'cats', 'tone': 'casual'})
        self.assertIsNone(error)
        self.assertIsNotNone(text)

    def test_get_prompt_replaces_placeholders(self, mock_gen):
        from ai_tools.generators.base import BaseGenerator
        gen = BaseGenerator()
        gen.system_prompt = 'Write about {topic} in {tone} tone.'
        gen.fields = [{'name': 'topic', 'label': 'Topic'}]
        prompt = gen.get_prompt({'topic': 'dogs', 'tone': 'formal'})
        self.assertEqual(prompt, 'Write about dogs in formal tone.')

    def test_to_dict(self, mock_gen):
        from ai_tools.generators.base import BaseGenerator
        gen = BaseGenerator()
        gen.slug = 'test'
        gen.name = 'Test Gen'
        gen.description = 'A test generator.'
        gen.category = 'general'
        d = gen.to_dict()
        self.assertEqual(d['slug'], 'test')
        self.assertEqual(d['name'], 'Test Gen')

    def test_premium_flag_passed_to_llm(self, mock_gen):
        from ai_tools.generators.base import BaseGenerator
        gen = BaseGenerator()
        gen.slug = 'test'
        gen.system_prompt = 'Write about {topic}.'
        gen.fields = [{'name': 'topic', 'label': 'Topic'}]
        gen.generate({'topic': 'test'}, use_premium=True)
        call_kwargs = mock_gen.call_args[1]
        self.assertTrue(call_kwargs.get('use_premium', False))


@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class GeneratorRegistryTests(TestCase):

    def test_registry_not_empty(self, mock_gen):
        from ai_tools.generators import GENERATOR_REGISTRY
        self.assertGreater(len(GENERATOR_REGISTRY), 0)

    def test_all_generators_have_required_fields(self, mock_gen):
        from ai_tools.generators import GENERATOR_REGISTRY
        for slug, gen in GENERATOR_REGISTRY.items():
            self.assertTrue(gen.slug, f'Generator {slug} missing slug')
            self.assertTrue(gen.name, f'Generator {slug} missing name')
            self.assertTrue(gen.category, f'Generator {slug} missing category')
            self.assertIsInstance(gen.fields, list, f'Generator {slug} fields not a list')

    def test_all_generators_can_generate(self, mock_gen):
        from ai_tools.generators import GENERATOR_REGISTRY
        for slug, gen in GENERATOR_REGISTRY.items():
            # Build minimal params from field definitions
            params = {}
            for field in gen.fields:
                params[field['name']] = 'test value'
            text, error = gen.generate(params)
            self.assertIsNone(error, f'Generator {slug} failed: {error}')
            self.assertIsNotNone(text, f'Generator {slug} returned None text')
