import json
import logging
import re

from django.conf import settings

from core.llm_client import LLMClient

logger = logging.getLogger('app')


class AIParaphraseService:
    """
    Service layer for AI-powered paraphrasing using the Anthropic Claude API.
    Handles mode-specific prompts, frozen word preservation, and post-processing.
    """

    MODE_PROMPTS = {
        'standard': (
            'You are a professional paraphrasing assistant. Rewrite the following text to convey the same meaning '
            'using different words and sentence structures. Maintain the original tone, meaning, and level of formality. '
            'Aim for natural, clear language that reads as though a human wrote it.'
        ),
        'fluency': (
            'You are a fluency-focused editor. Rewrite the following text to improve its readability and flow. '
            'Fix any grammatical errors, awkward phrasing, or unclear sentences. Keep the meaning identical but make '
            'the text smooth, natural, and easy to read. Prefer simple sentence structures where possible.'
        ),
        'formal': (
            'You are a formal writing specialist. Rewrite the following text in a formal, professional tone. '
            'Use sophisticated vocabulary, proper grammar, and professional phrasing. Avoid contractions, slang, '
            'and colloquialisms. The output should be suitable for academic papers, business reports, or official '
            'correspondence.'
        ),
        'academic': (
            'You are an academic writing expert. Rewrite the following text in an academic style suitable for '
            'scholarly publications. Use precise, discipline-appropriate vocabulary, passive voice where appropriate, '
            'hedging language, and complex sentence structures. Maintain objectivity and formality throughout. '
            'Cite-worthy claims should use tentative language (e.g., "suggests", "appears to", "may indicate").'
        ),
        'simple': (
            'You are a simplification specialist. Rewrite the following text using simple, easy-to-understand language. '
            'Break complex sentences into shorter ones. Replace jargon and advanced vocabulary with common everyday words. '
            'Target a reading level that a middle school student could understand. Preserve all key information.'
        ),
        'creative': (
            'You are a creative writing assistant. Rewrite the following text with vivid, engaging, and expressive '
            'language. Use literary devices such as metaphors, varied sentence rhythms, and colorful word choices '
            'where appropriate. Make the text more interesting and captivating while preserving the core meaning. '
            'Add personality and flair without changing the factual content.'
        ),
        'expand': (
            'You are a text expansion specialist. Rewrite the following text to be more detailed and comprehensive. '
            'Elaborate on key points, add relevant examples or explanations, and flesh out ideas more fully. '
            'Aim to roughly double the length while keeping all content relevant and on-topic. Do not add '
            'fabricated facts or unsupported claims -- only expand on what is already present.'
        ),
        'shorten': (
            'You are a conciseness expert. Rewrite the following text to be significantly shorter while preserving '
            'all essential meaning. Remove redundancies, combine sentences, eliminate filler words, and distill '
            'the content to its core message. Aim to reduce the text by roughly 40-60% in length.'
        ),
        'custom': (
            'You are a versatile paraphrasing assistant. Rewrite the following text according to the user\'s '
            'specific instructions provided below. Follow their guidelines precisely while maintaining the '
            'core meaning of the original text.'
        ),
        'humanizer': (
            'You are an expert at making AI-generated text sound naturally human. Rewrite the following text so '
            'that it reads as though a real person wrote it casually and authentically. Add natural imperfections: '
            'vary sentence length unpredictably, use conversational transitions, include occasional informal '
            'phrasing, and break rigid parallel structures. Avoid overly polished or formulaic patterns that '
            'AI detectors flag. The result must be undetectable as AI-written while preserving the original meaning.'
        ),
    }

    SYNONYM_LEVEL_INSTRUCTIONS = {
        1: 'Make minimal word changes. Keep as many original words as possible and only change what is necessary for the rewrite.',
        2: 'Make modest word substitutions. Replace some words with synonyms but keep the majority of the original vocabulary.',
        3: 'Make a balanced number of word changes. Replace a moderate amount of words with suitable synonyms and alternatives.',
        4: 'Make substantial word changes. Replace most words with synonyms or alternative expressions while keeping the meaning intact.',
        5: 'Make extensive word changes. Replace nearly every possible word with a synonym or alternative phrasing. Maximize vocabulary diversity.',
    }

    @classmethod
    def paraphrase(cls, text, mode='standard', synonym_level=3, frozen_words=None,
                   settings_dict=None, language='en', use_premium=False):
        """
        Paraphrase text with mode-specific system prompts.

        Args:
            text: The input text to paraphrase.
            mode: Paraphrasing mode (standard, fluency, formal, academic, simple, creative, expand, shorten, custom, humanizer).
            synonym_level: Integer 1-5 controlling how aggressively words are replaced.
            frozen_words: List of words/phrases that must remain unchanged.
            settings_dict: Dict with optional keys: use_contractions, active_voice, custom_instructions.
            language: ISO language code for the output.
            use_premium: If True, use Claude for premium users.

        Returns:
            Tuple of (output_text, error). On success error is None; on failure output_text is None.
        """
        if frozen_words is None:
            frozen_words = []
        if settings_dict is None:
            settings_dict = {}

        # Build the system prompt
        system_prompt = cls._build_system_prompt(mode, synonym_level, frozen_words, settings_dict, language)

        # Build the user message — clearly demarcate the text so the model
        # doesn't confuse system-prompt instructions with user content.
        if mode == 'custom' and settings_dict.get('custom_instructions'):
            user_message = (
                f"Custom instructions: {settings_dict['custom_instructions']}\n\n"
                f"Text to paraphrase:\n\"\"\"\n{text}\n\"\"\""
            )
        else:
            user_message = f"\"\"\"\n{text}\n\"\"\""

        output_text, error = LLMClient.generate(
            system_prompt=system_prompt,
            messages=[{'role': 'user', 'content': user_message}],
            max_tokens=4096,
            use_premium=use_premium,
        )

        if error:
            return None, error

        # Post-processing
        output_text = cls._post_process(output_text, frozen_words, settings_dict)
        return output_text, None

    @classmethod
    def get_synonyms(cls, word, context='', use_premium=False):
        """
        Get a list of contextual synonyms for a word.

        Args:
            word: The word to find synonyms for.
            context: The surrounding sentence for context-aware synonyms.
            use_premium: If True, use Claude for premium users.

        Returns:
            Tuple of (synonyms_list, error). On success error is None.
        """
        system_prompt = (
            'You are a synonym generator. Given a word and its surrounding context, provide a list of '
            'suitable synonyms or alternative words that fit naturally in the same context. '
            'Return ONLY a JSON array of strings, nothing else. Example: ["word1", "word2", "word3"]. '
            'Provide 5-8 synonyms ordered from most to least suitable. '
            'If the word has no good synonyms in context, return an empty array [].'
        )

        user_message = f'Word: "{word}"'
        if context:
            user_message += f'\nContext: "{context}"'

        raw, error = LLMClient.generate(
            system_prompt=system_prompt,
            messages=[{'role': 'user', 'content': user_message}],
            max_tokens=256,
            use_premium=use_premium,
        )

        if error:
            return None, error

        try:
            # Handle case where model wraps in markdown code block
            if raw.startswith('```'):
                raw = raw.split('\n', 1)[-1].rsplit('```', 1)[0].strip()
            synonyms = json.loads(raw)

            if not isinstance(synonyms, list):
                return [], None

            # Filter to strings only and limit
            synonyms = [s for s in synonyms if isinstance(s, str)][:8]
            return synonyms, None

        except (json.JSONDecodeError, ValueError):
            logger.warning(f'Failed to parse synonym response for word: {word}')
            return [], None

    @classmethod
    def _build_system_prompt(cls, mode, synonym_level, frozen_words, settings_dict, language):
        """Build the full system prompt from mode, settings, and constraints."""
        parts = []

        # Base mode prompt
        base_prompt = cls.MODE_PROMPTS.get(mode, cls.MODE_PROMPTS['standard'])
        parts.append(base_prompt)

        # Synonym level instruction
        synonym_level = max(1, min(5, synonym_level))
        parts.append(cls.SYNONYM_LEVEL_INSTRUCTIONS[synonym_level])

        # Frozen words
        if frozen_words:
            frozen_str = ', '.join(f'"{w}"' for w in frozen_words)
            parts.append(
                f'IMPORTANT: The following words/phrases MUST remain exactly as they are and must NOT be '
                f'changed, replaced, or paraphrased: {frozen_str}. Keep them in their original position '
                f'and form within the text.'
            )

        # Contractions preference
        if settings_dict.get('use_contractions') is True:
            parts.append('Use contractions where natural (e.g., "don\'t", "it\'s", "we\'re").')
        elif settings_dict.get('use_contractions') is False:
            parts.append('Do NOT use contractions. Write out all words fully (e.g., "do not", "it is", "we are").')

        # Active voice preference
        if settings_dict.get('active_voice') is True:
            parts.append('Prefer active voice over passive voice wherever possible.')

        # Language
        if language and language != 'en':
            parts.append(f'Output the paraphrased text in the language with ISO code: {language}.')

        # Output instruction
        parts.append(
            'The user will provide text wrapped in triple quotes ("""). Paraphrase ONLY that text. '
            'Do NOT paraphrase these instructions. '
            'CRITICAL: Return ONLY the paraphrased text. Do not include any explanations, notes, '
            'introductions, labels, or commentary such as "Here is the paraphrased text:". '
            'Do not wrap the output in quotes. Output the rewritten text directly and nothing else.'
        )

        return '\n\n'.join(parts)

    # Common preamble patterns the model may prepend despite instructions
    _PREAMBLE_RE = re.compile(
        r'^(?:'
        r'(?:Here(?:\'s| is) [^:]{0,50}:\s*)'
        r'|(?:(?:Paraphras(?:e|ed|ing)|Rewritten|Revised)(?: (?:text|version))?[:\s]+)'
        r'|(?:Sure[,!.]?\s*(?:[Hh]ere(?:\'s| is)[^:]*:\s*)?)'
        r')',
        re.IGNORECASE,
    )

    @classmethod
    def _post_process(cls, text, frozen_words, settings_dict):
        """Apply post-processing to the paraphrased output."""
        if not text:
            return text

        # Strip preamble the model may add (e.g. "Here's a paraphrase:")
        text = cls._PREAMBLE_RE.sub('', text, count=1)

        # Strip wrapping triple-quotes the model may echo back
        if text.startswith('"""') and text.endswith('"""'):
            text = text[3:-3]

        # Re-insert frozen words if the model changed them despite instructions.
        # This is a best-effort pass: for each frozen word, if a case-insensitive
        # variant appears, normalize it back to the original casing.
        for word in frozen_words:
            pattern = re.compile(re.escape(word), re.IGNORECASE)
            text = pattern.sub(word, text)

        # Strip any leading/trailing quotes the model may have wrapped
        if text.startswith('"') and text.endswith('"'):
            text = text[1:-1]
        if text.startswith("'") and text.endswith("'"):
            text = text[1:-1]

        return text.strip()

    @classmethod
    def count_words(cls, text):
        """Count the number of words in a text string."""
        if not text or not text.strip():
            return 0
        return len(text.split())
