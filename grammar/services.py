import json
import logging
import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class AIGrammarService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = getattr(settings, 'ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')

    def check_grammar(self, text, dialect='en-us'):
        """
        Check grammar and score writing quality.
        Returns (result_dict, error_string).
        result_dict contains 'corrections' list and 'writing_scores' dict.
        """
        prompt = f"""You are an expert grammar checker and writing analyst. Analyze the following text for grammar, spelling, punctuation, and style issues.

Dialect: {dialect}

Text to analyze:
\"\"\"
{text}
\"\"\"

Return a JSON object with exactly this structure:
{{
  "corrections": [
    {{
      "original": "the exact text with the error",
      "suggestion": "the corrected text",
      "type": "grammar|spelling|punctuation|style|clarity|wordiness|passive_voice",
      "explanation": "brief explanation of why this is an error and how to fix it",
      "position": {{
        "start": 0,
        "end": 10
      }}
    }}
  ],
  "writing_scores": {{
    "grammar": 85,
    "fluency": 78,
    "clarity": 82,
    "engagement": 70,
    "delivery": 75
  }},
  "tone": "formal|semi-formal|neutral|semi-casual|casual",
  "readability_score": 65.5
}}

Important rules:
- Each score must be an integer from 0-100
- "position" start/end are character indices in the original text
- Only flag genuine errors or meaningful improvements
- Be precise with positions - they must exactly match the original text
- readability_score should be the Flesch-Kincaid reading ease score (0-100)
- Return ONLY valid JSON, no markdown formatting or extra text"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = response.content[0].text.strip()

            # Strip markdown code fences if present
            if response_text.startswith('```'):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:])
                if response_text.endswith('```'):
                    response_text = response_text[:-3].strip()

            result = json.loads(response_text)

            # Validate structure
            if 'corrections' not in result:
                result['corrections'] = []
            if 'writing_scores' not in result:
                result['writing_scores'] = {
                    'grammar': 50, 'fluency': 50, 'clarity': 50,
                    'engagement': 50, 'delivery': 50
                }
            if 'tone' not in result:
                result['tone'] = 'neutral'
            if 'readability_score' not in result:
                result['readability_score'] = 50.0

            # Clamp scores to 0-100
            for key in ['grammar', 'fluency', 'clarity', 'engagement', 'delivery']:
                score = result['writing_scores'].get(key, 50)
                result['writing_scores'][key] = max(0, min(100, int(score)))

            return result, None

        except json.JSONDecodeError as e:
            logger.error(f"Grammar check JSON parse error: {e}")
            return None, "Failed to parse AI response"
        except anthropic.APIError as e:
            logger.error(f"Grammar check API error: {e}")
            return None, "AI service temporarily unavailable"
        except Exception as e:
            logger.error(f"Grammar check error: {e}")
            return None, str(e)

    def fix_all(self, text, corrections):
        """
        Apply all corrections to the text at once.
        Processes corrections from end to start to preserve character positions.
        Returns (corrected_text, error_string).
        """
        try:
            if not corrections:
                return text, None

            # Sort by position start descending so we fix from end to beginning
            sorted_corrections = sorted(
                corrections,
                key=lambda c: c.get('position', {}).get('start', 0),
                reverse=True
            )

            result = text
            for correction in sorted_corrections:
                pos = correction.get('position', {})
                start = pos.get('start')
                end = pos.get('end')
                suggestion = correction.get('suggestion', '')

                if start is not None and end is not None:
                    # Verify the original text matches before replacing
                    original_at_pos = result[start:end]
                    expected_original = correction.get('original', '')

                    if original_at_pos == expected_original:
                        result = result[:start] + suggestion + result[end:]
                    else:
                        # Fall back to simple string replace for the first occurrence
                        if expected_original in result:
                            result = result.replace(expected_original, suggestion, 1)

            return result, None

        except Exception as e:
            logger.error(f"Fix all error: {e}")
            return None, str(e)

    def fix_single(self, text, correction):
        """
        Apply a single correction to the text.
        Returns (corrected_text, error_string).
        """
        try:
            pos = correction.get('position', {})
            start = pos.get('start')
            end = pos.get('end')
            suggestion = correction.get('suggestion', '')
            original = correction.get('original', '')

            if start is not None and end is not None:
                original_at_pos = text[start:end]
                if original_at_pos == original:
                    return text[:start] + suggestion + text[end:], None

            # Fallback: replace first occurrence
            if original and original in text:
                return text.replace(original, suggestion, 1), None

            return text, "Could not locate the text to fix"

        except Exception as e:
            logger.error(f"Fix single error: {e}")
            return None, str(e)
