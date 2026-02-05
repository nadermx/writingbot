import json
import logging
import re

import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class AIHumanizerService:

    @staticmethod
    def humanize(text, mode='basic'):
        """
        Rewrite AI-generated text to sound more human.

        Args:
            text: The AI-generated text to humanize
            mode: 'basic' for light touch, 'advanced' for deep rewrite

        Returns:
            tuple: (result_dict, error_string)
            result_dict contains: output_text, ai_score_before, ai_score_after
        """
        if not text or not text.strip():
            return None, 'Please provide text to humanize.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

            # First, assess the AI score of the input
            score_prompt = f"""Analyze this text and estimate how likely it is to be AI-generated.
Return ONLY a JSON object with this format: {{"ai_score": 75}}
The score should be 0-100 where 100 = definitely AI generated.

Text:
{text}"""

            score_response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=256,
                messages=[{"role": "user", "content": score_prompt}]
            )

            score_text = score_response.content[0].text.strip()
            json_match = re.search(r'\{[\s\S]*?\}', score_text)
            if json_match:
                score_data = json.loads(json_match.group())
                ai_score_before = max(0, min(100, score_data.get('ai_score', 70)))
            else:
                ai_score_before = 70

            # Humanize the text based on mode
            if mode == 'advanced':
                humanize_prompt = f"""Rewrite the following text to make it sound completely human-written. Apply deep transformations:

1. Vary sentence structure significantly - mix short punchy sentences with longer ones
2. Add natural imperfections - contractions, informal transitions, occasional colloquialisms
3. Replace overused AI words (furthermore, moreover, additionally, delve, tapestry, multifaceted, nuanced, comprehensive, robust, leverage) with simpler alternatives
4. Add personal touches - first person where appropriate, rhetorical questions, anecdotes-style phrasing
5. Break up overly structured paragraphs
6. Use more concrete/specific language instead of abstract generalizations
7. Vary paragraph lengths - some short, some longer
8. Remove robotic transition phrases and replace with more natural flow
9. Add occasional sentence fragments or casual asides for naturalness
10. Maintain the original meaning and key information

IMPORTANT: Return ONLY the rewritten text. Do not include any explanations, notes, or metadata.

Text to rewrite:
{text}"""
            else:
                humanize_prompt = f"""Lightly rewrite the following text to reduce obvious AI patterns while keeping it close to the original:

1. Replace commonly flagged AI words (furthermore, moreover, additionally, delve, tapestry, multifaceted, nuanced, comprehensive, robust) with simpler alternatives
2. Add some contractions where natural (do not -> don't, it is -> it's)
3. Slightly vary sentence openings that follow repetitive patterns
4. Soften overly formal transitions
5. Keep the structure and meaning nearly identical to the original

IMPORTANT: Return ONLY the rewritten text. Do not include any explanations, notes, or metadata.

Text to rewrite:
{text}"""

            humanize_response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=4096,
                messages=[{"role": "user", "content": humanize_prompt}]
            )

            output_text = humanize_response.content[0].text.strip()

            # Score the output
            score_after_prompt = f"""Analyze this text and estimate how likely it is to be AI-generated.
Return ONLY a JSON object with this format: {{"ai_score": 25}}
The score should be 0-100 where 100 = definitely AI generated.

Text:
{output_text}"""

            score_after_response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=256,
                messages=[{"role": "user", "content": score_after_prompt}]
            )

            score_after_text = score_after_response.content[0].text.strip()
            json_match = re.search(r'\{[\s\S]*?\}', score_after_text)
            if json_match:
                score_after_data = json.loads(json_match.group())
                ai_score_after = max(0, min(100, score_after_data.get('ai_score', 30)))
            else:
                # Estimate reduction based on mode
                ai_score_after = max(5, ai_score_before - (40 if mode == 'advanced' else 25))

            return {
                'output_text': output_text,
                'ai_score_before': ai_score_before,
                'ai_score_after': ai_score_after,
            }, None

        except anthropic.APIError as e:
            logger.error(f'Anthropic API error in humanizer: {str(e)}')
            return None, 'Humanizer service is temporarily unavailable. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error in humanizer: {str(e)}')
            return None, 'An unexpected error occurred. Please try again.'
