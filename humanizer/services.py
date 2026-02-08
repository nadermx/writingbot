import json
import logging
import re

from core.llm_client import LLMClient, extract_json

logger = logging.getLogger('app')


class AIHumanizerService:

    @staticmethod
    def humanize(text, mode='basic', use_premium=False):
        """
        Rewrite AI-generated text to sound more human.

        Args:
            text: The AI-generated text to humanize
            mode: 'basic' for light touch, 'advanced' for deep rewrite
            use_premium: Whether to use premium model tier

        Returns:
            tuple: (result_dict, error_string)
            result_dict contains: output_text, ai_score_before, ai_score_after
        """
        if not text or not text.strip():
            return None, 'Please provide text to humanize.'

        try:
            # First, assess the AI score of the input
            score_prompt = f"""Analyze this text and estimate how likely it is to be AI-generated.
Return ONLY a JSON object with this format: {{"ai_score": 75}}
The score should be 0-100 where 100 = definitely AI generated.

Text:
{text}"""

            score_text, error = LLMClient.generate(
                system_prompt="You are an AI text detector.",
                messages=[{"role": "user", "content": score_prompt}],
                max_tokens=256,
                use_premium=use_premium
            )

            if error:
                return None, error

            try:
                score_data = extract_json(score_text)
                if isinstance(score_data, dict):
                    ai_score_before = max(0, min(100, int(score_data.get('ai_score', 70))))
                elif isinstance(score_data, (int, float)):
                    ai_score_before = max(0, min(100, int(score_data)))
                else:
                    ai_score_before = 70
            except (ValueError, json.JSONDecodeError, TypeError):
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

            output_text, error = LLMClient.generate(
                system_prompt="You are a professional text rewriter who makes AI text sound human.",
                messages=[{"role": "user", "content": humanize_prompt}],
                max_tokens=4096,
                use_premium=use_premium
            )

            if error:
                return None, error

            output_text = output_text.strip()

            # Score the output
            score_after_prompt = f"""Analyze this text and estimate how likely it is to be AI-generated.
Return ONLY a JSON object with this format: {{"ai_score": 25}}
The score should be 0-100 where 100 = definitely AI generated.

Text:
{output_text}"""

            score_after_text, error = LLMClient.generate(
                system_prompt="You are an AI text detector.",
                messages=[{"role": "user", "content": score_after_prompt}],
                max_tokens=256,
                use_premium=use_premium
            )

            if error:
                return None, error

            try:
                score_after_data = extract_json(score_after_text)
                if isinstance(score_after_data, dict):
                    ai_score_after = max(0, min(100, int(score_after_data.get('ai_score', 30))))
                elif isinstance(score_after_data, (int, float)):
                    ai_score_after = max(0, min(100, int(score_after_data)))
                else:
                    ai_score_after = max(5, ai_score_before - (40 if mode == 'advanced' else 25))
            except (ValueError, json.JSONDecodeError, TypeError):
                ai_score_after = max(5, ai_score_before - (40 if mode == 'advanced' else 25))

            return {
                'output_text': output_text,
                'ai_score_before': ai_score_before,
                'ai_score_after': ai_score_after,
            }, None

        except Exception as e:
            logger.error(f'Unexpected error in humanizer: {str(e)}')
            return None, 'An unexpected error occurred. Please try again.'
