import json
import logging
import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class AISummarizerService:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = getattr(settings, 'ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')

    # Map length 1-5 to approximate percentage of original
    LENGTH_MAP = {
        1: 10,
        2: 20,
        3: 30,
        4: 40,
        5: 50,
    }

    def summarize(self, text, mode='paragraph', length=3):
        """
        Summarize the given text.
        mode: 'key_sentences' or 'paragraph'
        length: 1-5 (shortest to longest)
        Returns (result_dict, error_string).
        """
        length = max(1, min(5, int(length)))
        target_pct = self.LENGTH_MAP.get(length, 30)

        word_count = len(text.split())
        target_words = max(20, int(word_count * target_pct / 100))

        if mode == 'key_sentences':
            mode_instruction = f"""Extract the most important sentences from the text.
Return them as a JSON array of strings under the key "sentences".
Select approximately {target_words} words worth of key sentences.
Preserve the original wording exactly - do not paraphrase.
Order them as they appear in the original text."""
        else:
            mode_instruction = f"""Write a condensed paragraph summary of the text.
The summary should be approximately {target_words} words.
Use clear, concise language that captures all key points.
Return the summary as a string under the key "paragraph"."""

        prompt = f"""You are an expert text summarizer. Summarize the following text.

{mode_instruction}

Text to summarize:
\"\"\"
{text}
\"\"\"

Return ONLY a valid JSON object with this structure:
{{
  {"'sentences': ['sentence 1', 'sentence 2', ...]" if mode == 'key_sentences' else "'paragraph': 'Your summary paragraph here.'"}
}}

Return ONLY valid JSON, no markdown formatting or extra text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
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

            # Build the summary text
            if mode == 'key_sentences':
                sentences = result.get('sentences', [])
                summary_text = '\n'.join(f'- {s}' for s in sentences) if sentences else ''
                sentence_count = len(sentences)
            else:
                summary_text = result.get('paragraph', '')
                sentence_count = len([s for s in summary_text.split('.') if s.strip()])

            summary_words = len(summary_text.split())
            original_words = len(text.split())
            reduction_pct = round((1 - summary_words / max(original_words, 1)) * 100, 1)

            return {
                'summary': summary_text,
                'mode': mode,
                'sentences': result.get('sentences', []) if mode == 'key_sentences' else [],
                'stats': {
                    'original_words': original_words,
                    'summary_words': summary_words,
                    'reduction_percent': reduction_pct,
                    'sentence_count': sentence_count,
                }
            }, None

        except json.JSONDecodeError as e:
            logger.error(f"Summarizer JSON parse error: {e}")
            return None, "Failed to parse AI response"
        except anthropic.APIError as e:
            logger.error(f"Summarizer API error: {e}")
            return None, "AI service temporarily unavailable"
        except Exception as e:
            logger.error(f"Summarizer error: {e}")
            return None, str(e)
