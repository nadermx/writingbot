import json
import logging

import requests
from django.conf import settings

logger = logging.getLogger('app')


LANGUAGES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'cs': 'Czech',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'et': 'Estonian',
    'fa': 'Persian',
    'fi': 'Finnish',
    'fr': 'French',
    'ga': 'Irish',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hr': 'Croatian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'id': 'Indonesian',
    'is': 'Icelandic',
    'it': 'Italian',
    'ja': 'Japanese',
    'ka': 'Georgian',
    'kk': 'Kazakh',
    'km': 'Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ms': 'Malay',
    'my': 'Myanmar',
    'ne': 'Nepali',
    'nl': 'Dutch',
    'no': 'Norwegian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'si': 'Sinhala',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tl': 'Filipino',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
    'zh': 'Chinese',
}


class TranslationService:
    API_URL = 'https://translateapi.ai/api/v1'

    @staticmethod
    def get_languages():
        """Return list of supported languages."""
        return [
            {'code': code, 'name': name}
            for code, name in sorted(LANGUAGES.items(), key=lambda x: x[1])
        ]

    @staticmethod
    def detect_language(text):
        """
        Auto-detect the source language of the text using translateapi.ai.

        Returns:
            tuple: (language_code, error_string)
        """
        try:
            response = requests.post(
                f'{TranslationService.API_URL}/detect/',
                headers={
                    'Authorization': f'Bearer {settings.TRANSLATEAPI_KEY}',
                    'Content-Type': 'application/json',
                },
                json={'text': text[:500]},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                lang_code = data.get('language', data.get('detected_language', 'en'))
                return lang_code, None
            else:
                logger.error(f'TranslateAPI detect error: {response.status_code} - {response.text}')
                return 'en', None  # Default to English on error

        except requests.Timeout:
            logger.error('TranslateAPI detect timeout')
            return 'en', None
        except Exception as e:
            logger.error(f'TranslateAPI detect error: {str(e)}')
            return 'en', None

    @staticmethod
    def translate(text, source_lang, target_lang):
        """
        Translate text using translateapi.ai API.

        Args:
            text: Text to translate
            source_lang: Source language code (or 'auto' for auto-detect)
            target_lang: Target language code

        Returns:
            tuple: (result_dict, error_string)
            result_dict contains: translated_text, source_lang, target_lang
        """
        if not text or not text.strip():
            return None, 'Please provide text to translate.'

        if not target_lang:
            return None, 'Please select a target language.'

        # Auto-detect source language if needed
        detected_lang = source_lang
        if source_lang == 'auto' or not source_lang:
            detected_lang, _ = TranslationService.detect_language(text)

        if detected_lang == target_lang:
            return {
                'translated_text': text,
                'source_lang': detected_lang,
                'target_lang': target_lang,
            }, None

        try:
            response = requests.post(
                f'{TranslationService.API_URL}/translate/',
                headers={
                    'Authorization': f'Bearer {settings.TRANSLATEAPI_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'text': text,
                    'source_language': detected_lang,
                    'target_language': target_lang,
                },
                timeout=30,
            )

            if response.status_code == 200:
                data = response.json()
                translated_text = data.get('translated_text', data.get('translation', ''))

                if not translated_text:
                    return None, 'Translation returned empty result. Please try again.'

                return {
                    'translated_text': translated_text,
                    'source_lang': detected_lang,
                    'target_lang': target_lang,
                }, None
            elif response.status_code == 429:
                return None, 'Translation rate limit reached. Please wait a moment and try again.'
            elif response.status_code == 401:
                logger.error('TranslateAPI authentication failed')
                return None, 'Translation service configuration error. Please contact support.'
            else:
                logger.error(f'TranslateAPI error: {response.status_code} - {response.text}')
                return None, 'Translation service is temporarily unavailable. Please try again.'

        except requests.Timeout:
            logger.error('TranslateAPI translate timeout')
            return None, 'Translation request timed out. Please try again with shorter text.'
        except requests.ConnectionError:
            logger.error('TranslateAPI connection error')
            return None, 'Could not connect to translation service. Please try again.'
        except Exception as e:
            logger.error(f'TranslateAPI unexpected error: {str(e)}')
            return None, 'An unexpected error occurred. Please try again.'
