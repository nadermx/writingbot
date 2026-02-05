import json
import logging

import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class FlowService:
    """
    Service layer for AI-powered writing assistance in the Flow co-writer.
    Uses the Anthropic Claude API for suggestions, reviews, outlines, and smart starts.
    """

    @classmethod
    def suggest_next(cls, document_content, cursor_position=None):
        """
        Suggest the next sentence(s) based on document content and cursor position.

        Args:
            document_content: The full document text (HTML stripped by caller or raw text).
            cursor_position: Optional integer character offset of the cursor.

        Returns:
            Tuple of (suggestion_text, error). On success error is None.
        """
        system_prompt = (
            'You are an expert writing assistant embedded in a document editor. '
            'Given the document content so far, suggest the next 1-2 sentences that naturally '
            'continue the writing. Match the tone, style, and subject matter of the existing text. '
            'If the text appears to be an outline or structured document, suggest content that fits '
            'the current section. Return ONLY the suggested text with no explanations, labels, or commentary.'
        )

        # If cursor_position is provided, use text up to that point
        text = document_content or ''
        if cursor_position is not None:
            try:
                cursor_position = int(cursor_position)
                text = text[:cursor_position]
            except (ValueError, TypeError):
                pass

        if not text.strip():
            return 'Start writing your document here...', None

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=512,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': f'Continue this text:\n\n{text}'}
                ]
            )
            suggestion = response.content[0].text.strip()
            return suggestion, None

        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during suggest_next')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during suggest_next: {e}')
            return None, 'An error occurred while generating suggestions. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during suggest_next: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    @classmethod
    def ai_review(cls, document_content):
        """
        Review a document and provide feedback on clarity, tone, style, and structure.

        Args:
            document_content: The full document text.

        Returns:
            Tuple of (review_dict, error). review_dict has keys: summary, clarity, tone, style, structure, suggestions.
        """
        system_prompt = (
            'You are a professional writing coach and editor. Review the following document and provide '
            'detailed, actionable feedback. Return your review as a JSON object with exactly these keys:\n'
            '- "summary": A brief 1-2 sentence overall assessment.\n'
            '- "clarity": Feedback on how clear and understandable the writing is (1-2 sentences).\n'
            '- "tone": Assessment of the tone and voice consistency (1-2 sentences).\n'
            '- "style": Comments on writing style, word choice, and readability (1-2 sentences).\n'
            '- "structure": Feedback on organization, flow, and paragraph structure (1-2 sentences).\n'
            '- "suggestions": An array of 3-5 specific, actionable improvement suggestions (strings).\n'
            '- "score": An overall quality score from 1-100.\n\n'
            'Return ONLY the JSON object. No markdown code fences, no extra text.'
        )

        if not document_content or not document_content.strip():
            return None, 'Please provide some text to review.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': f'Review this document:\n\n{document_content}'}
                ]
            )
            raw = response.content[0].text.strip()

            # Handle markdown code block wrapping
            if raw.startswith('```'):
                raw = raw.split('\n', 1)[-1].rsplit('```', 1)[0].strip()

            review = json.loads(raw)
            return review, None

        except json.JSONDecodeError:
            logger.warning('Failed to parse AI review response as JSON')
            return None, 'Failed to parse the review. Please try again.'
        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during ai_review')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during ai_review: {e}')
            return None, 'An error occurred while reviewing your document. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during ai_review: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    @classmethod
    def smart_start(cls, keywords):
        """
        Generate a document outline from keywords to help users get started.

        Args:
            keywords: A string of keywords or a brief topic description.

        Returns:
            Tuple of (outline_html, error). outline_html is HTML-formatted outline content.
        """
        system_prompt = (
            'You are an expert writing assistant that helps writers get started. Given a set of keywords '
            'or a topic, generate a well-structured document outline. The outline should include:\n'
            '- A suggested title\n'
            '- An introduction section\n'
            '- 3-5 main sections with brief descriptions of what to cover\n'
            '- A conclusion section\n\n'
            'Format the output as clean HTML suitable for a rich text editor using these tags only: '
            '<h1> for the title, <h2> for section headings, <p> for descriptions and placeholder text, '
            '<ul> and <li> for sub-points. Do NOT include <html>, <head>, <body>, or <style> tags. '
            'Return ONLY the HTML content. No explanations or commentary.'
        )

        if not keywords or not keywords.strip():
            return None, 'Please provide keywords or a topic to generate an outline.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=2048,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': f'Generate a document outline for: {keywords}'}
                ]
            )
            outline = response.content[0].text.strip()

            # Strip markdown code fences if present
            if outline.startswith('```'):
                outline = outline.split('\n', 1)[-1].rsplit('```', 1)[0].strip()

            return outline, None

        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during smart_start')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during smart_start: {e}')
            return None, 'An error occurred while generating the outline. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during smart_start: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    @classmethod
    def research_search(cls, query):
        """
        Placeholder for web search integration for the research sidebar.

        Args:
            query: Search query string.

        Returns:
            Tuple of (results_list, error). Each result is a dict with title, snippet, url.
        """
        if not query or not query.strip():
            return None, 'Please enter a search query.'

        # Placeholder: in production, integrate with a web search API
        # (e.g., Brave Search, SerpAPI, Google Custom Search)
        results = [
            {
                'title': f'Search results for "{query}"',
                'snippet': 'Web search integration is coming soon. This is a placeholder result.',
                'url': '#',
            }
        ]
        return results, None

    @classmethod
    def generate_outline(cls, topic):
        """
        Generate a structured outline for a given topic.

        Args:
            topic: The topic or subject to outline.

        Returns:
            Tuple of (outline_data, error). outline_data is a dict with title and sections.
        """
        system_prompt = (
            'You are a writing structure expert. Given a topic, generate a detailed outline '
            'as a JSON object with these keys:\n'
            '- "title": Suggested document title\n'
            '- "sections": Array of objects, each with "heading" (string) and "points" (array of strings)\n\n'
            'Include 4-6 sections with 2-4 points each. '
            'Return ONLY the JSON object. No markdown code fences, no extra text.'
        )

        if not topic or not topic.strip():
            return None, 'Please provide a topic.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': f'Generate an outline for: {topic}'}
                ]
            )
            raw = response.content[0].text.strip()

            if raw.startswith('```'):
                raw = raw.split('\n', 1)[-1].rsplit('```', 1)[0].strip()

            outline = json.loads(raw)
            return outline, None

        except json.JSONDecodeError:
            logger.warning('Failed to parse outline response as JSON')
            return None, 'Failed to parse the outline. Please try again.'
        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during generate_outline')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during generate_outline: {e}')
            return None, 'An error occurred while generating the outline. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during generate_outline: {e}')
            return None, 'An unexpected error occurred. Please try again.'
