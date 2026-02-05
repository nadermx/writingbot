"""Tests for the citations service (no LLM needed)."""
from django.test import TestCase


class CitationsPageTests(TestCase):

    def test_citations_page_loads(self):
        response = self.client.get('/citation-generator/')
        self.assertEqual(response.status_code, 200)
