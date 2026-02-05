"""Tests for media tools services (non-LLM operations)."""
import unittest

from django.test import TestCase

try:
    import qrcode
    HAS_QRCODE = True
except ImportError:
    HAS_QRCODE = False

try:
    import wordcloud
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False


@unittest.skipUnless(HAS_QRCODE, 'qrcode package not installed')
class QRServiceTests(TestCase):

    def test_generate_qr_code(self):
        from media_tools.services import QRService
        result, error = QRService.generate_qr_code(
            data='https://writingbot.ai',
            size=200,
            fg_color='#000000',
            bg_color='#FFFFFF',
        )
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_generate_qr_code_empty_data(self):
        from media_tools.services import QRService
        result, error = QRService.generate_qr_code(data='')
        self.assertIsNone(result)
        self.assertIsNotNone(error)


@unittest.skipUnless(HAS_WORDCLOUD, 'wordcloud package not installed')
class WordCloudServiceTests(TestCase):

    def test_generate_word_cloud(self):
        from media_tools.services import WordCloudService
        text = 'writing tools AI paraphraser grammar checker summarizer word cloud test'
        result, error = WordCloudService.generate_word_cloud(text)
        self.assertIsNone(error)
        self.assertIsNotNone(result)

    def test_generate_word_cloud_empty(self):
        from media_tools.services import WordCloudService
        result, error = WordCloudService.generate_word_cloud('')
        self.assertIsNone(result)
        self.assertIsNotNone(error)


class VoiceServiceTests(TestCase):

    def test_voice_mapping(self):
        from media_tools.services import VoiceService
        # Check that all voice IDs are valid
        self.assertIn('alloy', VoiceService.VOICES)
        self.assertIn('echo', VoiceService.VOICES)
