import json
import logging
import re
import math

import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class AIDetectorService:
    CLASSIFICATION_THRESHOLDS = {
        'ai_generated': 80,
        'ai_refined': 60,
        'human_refined': 30,
    }

    @staticmethod
    def _get_classification(score):
        if score >= 80:
            return 'ai_generated'
        elif score >= 60:
            return 'ai_refined'
        elif score >= 30:
            return 'human_refined'
        else:
            return 'human_written'

    @staticmethod
    def _get_label(score):
        if score >= 80:
            return 'AI Generated'
        elif score >= 60:
            return 'AI Refined'
        elif score >= 30:
            return 'Human Refined'
        else:
            return 'Human Written'

    @staticmethod
    def _get_color(score):
        if score >= 80:
            return 'red'
        elif score >= 60:
            return 'orange'
        elif score >= 30:
            return 'yellow'
        else:
            return 'green'

    @staticmethod
    def _split_sentences(text):
        """Split text into sentences."""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def _compute_perplexity_heuristics(text):
        """
        Compute simple perplexity-based heuristics for AI detection.
        Returns a base score adjustment based on text characteristics.
        """
        sentences = AIDetectorService._split_sentences(text)
        if not sentences:
            return 0

        # Heuristic 1: Sentence length uniformity (AI tends to be uniform)
        lengths = [len(s.split()) for s in sentences]
        if len(lengths) > 1:
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = math.sqrt(variance) if variance > 0 else 0
            # Low variance = more AI-like
            uniformity_score = max(0, 10 - std_dev) * 2
        else:
            uniformity_score = 5

        # Heuristic 2: Vocabulary diversity (AI tends to use more diverse vocab)
        words = text.lower().split()
        if words:
            unique_ratio = len(set(words)) / len(words)
            # Very high unique ratio can indicate AI
            vocab_score = unique_ratio * 15
        else:
            vocab_score = 0

        # Heuristic 3: Common AI transition phrases
        ai_phrases = [
            'furthermore', 'moreover', 'additionally', 'in conclusion',
            'it is important to note', 'it is worth noting', 'in essence',
            'delve', 'tapestry', 'multifaceted', 'nuanced', 'comprehensive',
            'robust', 'leverage', 'paradigm', 'holistic', 'synergy',
            'in today\'s world', 'in today\'s digital age', 'in this article',
            'as we navigate', 'it\'s important to remember',
        ]
        text_lower = text.lower()
        phrase_count = sum(1 for phrase in ai_phrases if phrase in text_lower)
        phrase_score = min(phrase_count * 8, 30)

        return min(uniformity_score + vocab_score + phrase_score, 50)

    @staticmethod
    def detect(text):
        """
        Analyze text for AI-generated content using Claude + perplexity heuristics.

        Returns:
            tuple: (result_dict, error_string)
            result_dict contains: overall_score, classification, sentences
        """
        sentences = AIDetectorService._split_sentences(text)
        if not sentences:
            return None, 'No sentences found in the provided text.'

        # Get heuristic base score
        heuristic_score = AIDetectorService._compute_perplexity_heuristics(text)

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

            prompt = f"""Analyze the following text and determine if it was written by AI or a human.
For each sentence, provide a probability score from 0 to 100 indicating how likely it is AI-generated (100 = definitely AI, 0 = definitely human).

Consider these factors:
- Sentence structure patterns (AI tends to be more uniform)
- Vocabulary choices (AI uses certain words more frequently like "delve", "tapestry", "multifaceted")
- Transition phrases (AI relies heavily on "Furthermore", "Moreover", "Additionally")
- Natural imperfections (humans make more varied sentence constructions)
- Personal voice and style (humans tend to have more unique voice)
- Specificity vs generality (AI tends to be more general)

Return your analysis as a JSON object with this exact format:
{{
    "sentences": [
        {{"text": "sentence text here", "score": 75}},
        ...
    ],
    "overall_score": 65
}}

Text to analyze:
{text}

Return ONLY the JSON object, no other text."""

            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = response.content[0].text.strip()

            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if not json_match:
                return None, 'Failed to parse AI detection results.'

            result = json.loads(json_match.group())

            # Blend Claude's score with heuristic score
            claude_score = result.get('overall_score', 50)
            blended_score = round((claude_score * 0.7) + (heuristic_score * 0.3))
            blended_score = max(0, min(100, blended_score))

            # Process sentences
            analyzed_sentences = []
            for item in result.get('sentences', []):
                score = max(0, min(100, item.get('score', 50)))
                analyzed_sentences.append({
                    'text': item.get('text', ''),
                    'score': score,
                    'label': AIDetectorService._get_label(score),
                    'color': AIDetectorService._get_color(score),
                })

            # If Claude returned fewer sentences than we have, fill in
            if len(analyzed_sentences) < len(sentences):
                for i in range(len(analyzed_sentences), len(sentences)):
                    analyzed_sentences.append({
                        'text': sentences[i],
                        'score': blended_score,
                        'label': AIDetectorService._get_label(blended_score),
                        'color': AIDetectorService._get_color(blended_score),
                    })

            classification = AIDetectorService._get_classification(blended_score)

            return {
                'overall_score': blended_score,
                'classification': classification,
                'classification_label': AIDetectorService._get_label(blended_score),
                'sentences': analyzed_sentences,
            }, None

        except anthropic.APIError as e:
            logger.error(f'Anthropic API error in AI detector: {str(e)}')
            return None, 'AI detection service is temporarily unavailable. Please try again.'
        except json.JSONDecodeError as e:
            logger.error(f'JSON decode error in AI detector: {str(e)}')
            return None, 'Failed to parse AI detection results.'
        except Exception as e:
            logger.error(f'Unexpected error in AI detector: {str(e)}')
            return None, 'An unexpected error occurred. Please try again.'
