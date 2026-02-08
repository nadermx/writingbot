import json
import logging

from core.llm_client import LLMClient

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
        Auto-detect the source language using the LLM.

        Returns:
            tuple: (language_code, error_string)
        """
        system_prompt = (
            'You are a language detection tool. Identify the language of the given text. '
            'Respond with ONLY the ISO 639-1 two-letter language code (e.g., "en", "es", "fr", "de", "zh"). '
            'Do not include any other text, explanation, or punctuation.'
        )
        messages = [{'role': 'user', 'content': text[:500]}]

        result, error = LLMClient.generate(
            system_prompt=system_prompt,
            messages=messages,
            max_tokens=10,
            temperature=0.1,
        )

        if error or not result:
            logger.error(f'Language detection failed: {error}')
            return 'en', None  # Default to English on error

        lang_code = result.strip().lower().replace('"', '').replace("'", '')[:2]
        if lang_code in LANGUAGES:
            return lang_code, None

        return 'en', None

    @staticmethod
    def translate(text, source_lang, target_lang, use_premium=False):
        """
        Translate text using the LLM via api.writingbot.ai.

        Args:
            text: Text to translate
            source_lang: Source language code (or 'auto' for auto-detect)
            target_lang: Target language code
            use_premium: Whether to use premium (Claude) model

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

        source_name = LANGUAGES.get(detected_lang, detected_lang)
        target_name = LANGUAGES.get(target_lang, target_lang)

        system_prompt = (
            f'You are a professional translator. Translate the following text from {source_name} to {target_name}. '
            f'Provide ONLY the translated text. Do not include any explanations, notes, or the original text. '
            f'Preserve the original formatting, paragraph breaks, and punctuation style.'
        )
        messages = [{'role': 'user', 'content': text}]

        result, error = LLMClient.generate(
            system_prompt=system_prompt,
            messages=messages,
            max_tokens=min(len(text) * 3, 8192),
            temperature=0.3,
            use_premium=use_premium,
        )

        if error:
            logger.error(f'Translation LLM error: {error}')
            return None, 'Translation service is temporarily unavailable. Please try again.'

        if not result or not result.strip():
            return None, 'Translation returned empty result. Please try again.'

        return {
            'translated_text': result.strip(),
            'source_lang': detected_lang,
            'target_lang': target_lang,
        }, None
