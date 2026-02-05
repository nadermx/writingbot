"""Tests for the citations service (no LLM needed)."""
from django.test import TestCase


class CitationsPageTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        from translations.models.language import Language
        Language.objects.get_or_create(
            iso='en',
            defaults={'name': 'English', 'en_label': 'English'}
        )

    def test_citations_page_loads(self):
        response = self.client.get('/citation-generator/')
        self.assertEqual(response.status_code, 200)
