import json
import logging
from core.llm_client import LLMClient, extract_json

logger = logging.getLogger('app')


class AISummarizerService:
    def __init__(self):
        pass

    # Map length 1-5 to approximate percentage of original
    LENGTH_MAP = {
        1: 10,
        2: 20,
        3: 30,
        4: 40,
        5: 50,
    }

    def summarize(self, text, mode='paragraph', length=3, use_premium=False,
                  custom_instructions=None, keywords=None):
        """
        Summarize the given text.
        mode: 'key_sentences', 'paragraph', or 'custom'
        length: 1-5 (shortest to longest)
        use_premium: whether to use premium model
        custom_instructions: custom instructions for 'custom' mode (premium only)
        keywords: list of keywords to emphasize in the summary
        Returns (result_dict, error_string).
        """
        length = max(1, min(5, int(length)))
        target_pct = self.LENGTH_MAP.get(length, 30)

        word_count = len(text.split())
        target_words = max(20, int(word_count * target_pct / 100))

        # Build keyword instruction if provided
        keyword_instruction = ''
        if keywords and isinstance(keywords, list) and len(keywords) > 0:
            keyword_list = ', '.join(f'"{k}"' for k in keywords[:20])  # Cap at 20 keywords
            keyword_instruction = f"""
Pay special attention to and emphasize content related to these keywords: {keyword_list}.
Ensure the summary covers information related to these topics/terms when present in the text."""

        if mode == 'custom' and custom_instructions:
            mode_instruction = f"""Follow these custom instructions for summarizing:
{custom_instructions}

Target approximately {target_words} words for the output.
Return the result as a string under the key "paragraph"."""
        elif mode == 'key_sentences':
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

        # For custom mode, use paragraph format for output
        output_mode = 'key_sentences' if mode == 'key_sentences' else 'paragraph'

        prompt = f"""You are an expert text summarizer. Summarize the following text.

{mode_instruction}
{keyword_instruction}

Text to summarize:
\"\"\"
{text}
\"\"\"

Return ONLY a valid JSON object with this structure:
{{
  {"'sentences': ['sentence 1', 'sentence 2', ...]" if output_mode == 'key_sentences' else "'paragraph': 'Your summary paragraph here.'"}
}}

Return ONLY valid JSON, no markdown formatting or extra text."""

        try:
            response_text, error = LLMClient.generate(
                system_prompt="You are an expert text summarizer.",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2048,
                use_premium=use_premium
            )

            if error:
                return None, error

            result = extract_json(response_text)

            # Build the summary text
            if mode == 'key_sentences':
                sentences = result.get('sentences', [])
                summary_text = '\n'.join(f'- {s}' for s in sentences) if sentences else ''
                sentence_count = len(sentences)
            else:
                # Both 'paragraph' and 'custom' modes use paragraph output
                summary_text = result.get('paragraph', '')
                sentence_count = len([s for s in summary_text.split('.') if s.strip()])

            summary_words = len(summary_text.split())
            original_words = len(text.split())
            reduction_pct = round((1 - summary_words / max(original_words, 1)) * 100, 1)

            return {
                'summary': summary_text,
                'mode': mode,
                'sentences': result.get('sentences', []) if output_mode == 'key_sentences' else [],
                'stats': {
                    'original_words': original_words,
                    'summary_words': summary_words,
                    'reduction_percent': reduction_pct,
                    'sentence_count': sentence_count,
                }
            }, None

        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Summarizer JSON parse error: {e}")
            return None, "Failed to parse AI response"
        except Exception as e:
            logger.error(f"Summarizer error: {e}")
            return None, str(e)
