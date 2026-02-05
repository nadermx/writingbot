"""Tests for the plagiarism service (no LLM needed, uses DuckDuckGo)."""
from unittest.mock import patch

from django.test import TestCase


class PlagiarismServiceTests(TestCase):

    def test_split_into_segments(self):
        from plagiarism.services import PlagiarismService
        text = ' '.join(['word'] * 100)
        segments = PlagiarismService._split_into_segments(text, segment_size=30)
        self.assertGreater(len(segments), 0)
        self.assertLessEqual(len(segments), 10)

    def test_split_short_text(self):
        from plagiarism.services import PlagiarismService
        text = 'short text'
        segments = PlagiarismService._split_into_segments(text, segment_size=30)
        # Short text may produce 0 or 1 segments
        self.assertLessEqual(len(segments), 1)

    @patch('plagiarism.services.requests.get')
    def test_search_segment(self, mock_get):
        from plagiarism.services import PlagiarismService

        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '''
        <a class="result__a" href="https://example.com">Example Result</a>
        <a class="result__snippet">This is a matching snippet with similar content.</a>
        '''

        matches = PlagiarismService._search_segment('This is a matching snippet with similar content')
        self.assertIsInstance(matches, list)
