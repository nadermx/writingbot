"""
Shared fixtures and mock helpers for WritingBot tests.
"""
import json
from unittest.mock import patch, MagicMock

import django
from django.test import TestCase, RequestFactory, Client

# Ensure Django settings are configured
django.setup()


# ---------------------------------------------------------------
# Mock LLM responses
# ---------------------------------------------------------------

MOCK_PARAPHRASE_RESPONSE = 'The quick brown fox leaps over the idle canine.'

MOCK_GRAMMAR_RESPONSE = json.dumps({
    'corrections': [
        {
            'original': 'teh',
            'suggestion': 'the',
            'type': 'spelling',
            'explanation': 'Common misspelling',
            'position': {'start': 0, 'end': 3},
        }
    ],
    'writing_scores': {
        'grammar': 85,
        'fluency': 80,
        'clarity': 90,
        'engagement': 75,
        'delivery': 82,
    },
    'tone': 'informal',
    'readability_score': 72,
})

MOCK_SUMMARY_RESPONSE = json.dumps({
    'summary': 'This is a summary of the text.',
    'key_points': ['Point 1', 'Point 2'],
})

MOCK_AI_DETECT_RESPONSE = json.dumps({
    'classification': 'human_written_ai_refined',
    'category_confidences': {
        'ai_generated': 5,
        'ai_generated_ai_refined': 15,
        'human_written_ai_refined': 55,
        'human_written': 25,
    },
    'sentences': [
        {'text': 'This is a test sentence.', 'score': 45},
        {'text': 'Another sentence here.', 'score': 20},
    ],
    'overall_score': 32,
})

# Response from DeBERTa model endpoint (used by LLMClient.detect_ai_text)
MOCK_AI_DETECT_MODEL_RESPONSE = {
    'score': 72.5,
    'label': 'ai',
    'chunks': [72.5],
}

MOCK_HUMANIZE_SCORE_RESPONSE = '75'

MOCK_HUMANIZE_TEXT_RESPONSE = 'The cat sat on the mat, you know, just chilling there.'

MOCK_REVIEW_RESPONSE = json.dumps({
    'summary': 'Well-written document.',
    'clarity': 'Clear and concise.',
    'tone': 'Professional.',
    'style': 'Academic.',
    'structure': 'Well-organized.',
    'suggestions': ['Add more examples.', 'Expand the conclusion.'],
    'score': 82,
})

MOCK_OUTLINE_RESPONSE = '<h1>Title</h1><h2>Section 1</h2><p>Description</p>'

MOCK_OUTLINE_JSON_RESPONSE = json.dumps({
    'title': 'Test Outline',
    'sections': [
        {'heading': 'Introduction', 'points': ['Point 1', 'Point 2']},
        {'heading': 'Main Body', 'points': ['Point 3', 'Point 4']},
    ],
})

MOCK_CHAT_RESPONSE = 'Here are some tips for improving your writing...'

MOCK_SEARCH_RESPONSE = (
    'ANSWER:\nThis is a comprehensive answer about the topic.\n\n'
    'SOURCES_JSON:\n[{"title": "Source 1", "snippet": "Description of source 1"}]'
)

MOCK_SYNONYMS_RESPONSE = json.dumps(['quick', 'fast', 'rapid', 'swift', 'speedy'])

MOCK_LOGO_RESPONSE = 'Logo design: Modern minimalist mark with...'

MOCK_CHARACTER_RESPONSE = 'Character sheet: A tall elf warrior with...'

MOCK_BANNER_RESPONSE = 'Banner design: Bold typography with gradient...'

MOCK_PRESENTATION_RESPONSE = json.dumps({
    'title': 'Test Presentation',
    'slides': [
        {'title': 'Introduction', 'content': 'Welcome', 'notes': 'Speaker notes'},
    ],
})

MOCK_PDF_CHAT_RESPONSE = 'Based on the PDF content, the answer is...'

MOCK_IMAGE_PROMPT_RESPONSE = 'A photorealistic image of a sunset over mountains...'

MOCK_TRANSLATION_RESPONSE = 'Hola, como estas?'

MOCK_LANGUAGE_DETECT_RESPONSE = 'en'


def mock_llm_generate(system_prompt='', messages=None, max_tokens=4096,
                      temperature=0.7, use_premium=False):
    """
    Default mock for LLMClient.generate that returns reasonable responses
    based on the system prompt content.
    """
    prompt_lower = (system_prompt or '').lower()
    user_msg = messages[0]['content'] if messages else '' if not messages else ''

    if 'paraphras' in prompt_lower:
        return MOCK_PARAPHRASE_RESPONSE, None
    if 'grammar' in prompt_lower or 'corrections' in prompt_lower:
        return MOCK_GRAMMAR_RESPONSE, None
    if 'summar' in prompt_lower:
        return MOCK_SUMMARY_RESPONSE, None
    if 'ai' in prompt_lower and 'detect' in prompt_lower:
        return MOCK_AI_DETECT_RESPONSE, None
    if 'human' in prompt_lower and 'rewrite' in prompt_lower:
        return MOCK_HUMANIZE_TEXT_RESPONSE, None
    if 'review' in prompt_lower or 'coach' in prompt_lower:
        return MOCK_REVIEW_RESPONSE, None
    if 'outline' in prompt_lower and 'html' in prompt_lower:
        return MOCK_OUTLINE_RESPONSE, None
    if 'outline' in prompt_lower and 'json' in prompt_lower:
        return MOCK_OUTLINE_JSON_RESPONSE, None
    if 'synonym' in prompt_lower:
        return MOCK_SYNONYMS_RESPONSE, None
    if 'chat' in prompt_lower or 'writing assistant' in prompt_lower:
        return MOCK_CHAT_RESPONSE, None
    if 'research' in prompt_lower or 'search' in prompt_lower:
        return MOCK_SEARCH_RESPONSE, None
    if 'logo' in prompt_lower:
        return MOCK_LOGO_RESPONSE, None
    if 'character' in prompt_lower:
        return MOCK_CHARACTER_RESPONSE, None
    if 'banner' in prompt_lower:
        return MOCK_BANNER_RESPONSE, None
    if 'presentation' in prompt_lower or 'slide' in prompt_lower:
        return MOCK_PRESENTATION_RESPONSE, None
    if 'pdf' in prompt_lower or 'document' in prompt_lower:
        return MOCK_PDF_CHAT_RESPONSE, None
    if 'image' in prompt_lower:
        return MOCK_IMAGE_PROMPT_RESPONSE, None
    if 'language detection' in prompt_lower or ('detect' in prompt_lower and 'language' in prompt_lower):
        return MOCK_LANGUAGE_DETECT_RESPONSE, None
    if 'translat' in prompt_lower:
        return MOCK_TRANSLATION_RESPONSE, None

    # Default fallback
    return 'Mock LLM response for testing.', None
