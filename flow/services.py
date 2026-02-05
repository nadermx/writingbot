import hashlib
import json
import logging

import anthropic
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger('app')

# Rate limits for chat and search
CHAT_LIMITS = settings.TOOL_LIMITS.get('ai_chat', {})
CHAT_FREE_DAILY = CHAT_LIMITS.get('free_daily', 20)
SEARCH_LIMITS = settings.TOOL_LIMITS.get('ai_search', {})
SEARCH_FREE_DAILY = SEARCH_LIMITS.get('free_daily', 10)


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

    # ------------------------------------------------------------------
    # Rate limiting helpers for AI Chat and AI Search
    # ------------------------------------------------------------------

    @staticmethod
    def _ip_hash(ip, user_agent=''):
        raw = f'{ip}:{user_agent}'
        return hashlib.sha256(raw.encode()).hexdigest()

    @staticmethod
    def check_daily_limit(tool, user, ip, user_agent=''):
        """
        Check daily usage for a tool ('ai_chat' or 'ai_search').

        Returns:
            Tuple of (allowed: bool, remaining: int, limit: int).
            Premium users get (-1, -1) for unlimited.
        """
        from django.core.cache import cache

        is_premium = (
            user and user.is_authenticated
            and getattr(user, 'is_plan_active', False)
        )
        if is_premium:
            return True, -1, -1

        limit = CHAT_FREE_DAILY if tool == 'ai_chat' else SEARCH_FREE_DAILY

        today = timezone.now().strftime('%Y-%m-%d')
        if user and user.is_authenticated:
            cache_key = f'{tool}:user:{user.id}:{today}'
        else:
            ip_hash = FlowService._ip_hash(ip, user_agent)
            cache_key = f'{tool}:anon:{ip_hash}:{today}'

        count = cache.get(cache_key, 0)
        remaining = max(0, limit - count)
        return count < limit, remaining, limit

    @staticmethod
    def increment_daily_usage(tool, user, ip, user_agent=''):
        """Increment the daily usage counter in cache (expires at midnight)."""
        from django.core.cache import cache

        today = timezone.now().strftime('%Y-%m-%d')
        if user and user.is_authenticated:
            cache_key = f'{tool}:user:{user.id}:{today}'
        else:
            ip_hash = FlowService._ip_hash(ip, user_agent)
            cache_key = f'{tool}:anon:{ip_hash}:{today}'

        try:
            count = cache.get(cache_key, 0)
            cache.set(cache_key, count + 1, timeout=86400)
        except Exception as e:
            logger.error(f'Failed to increment daily usage for {tool}: {e}')

    # ------------------------------------------------------------------
    # AI Chat
    # ------------------------------------------------------------------

    @classmethod
    def chat(cls, message, history=None):
        """
        Send a message with conversation history to Claude and return the response.

        Args:
            message: The user's latest message string.
            history: List of dicts with 'role' ('user'|'assistant') and 'content'.

        Returns:
            Tuple of (response_text, error). On success error is None.
        """
        system_prompt = (
            'You are a helpful, friendly AI writing assistant on WritingBot.ai. '
            'You help users with writing tasks such as brainstorming ideas, improving '
            'their writing, explaining grammar rules, suggesting outlines, and answering '
            'questions about writing, language, and communication. '
            'Be concise but thorough. Use markdown formatting in your responses when '
            'appropriate (headings, bullet points, bold, code blocks, etc.). '
            'If the user asks something outside the scope of writing and language, '
            'you may still answer helpfully but gently steer back to writing topics.'
        )

        if not message or not message.strip():
            return None, 'Please enter a message.'

        # Build the messages list from history + current message
        messages = []
        if history:
            for entry in history:
                role = entry.get('role', '')
                content = entry.get('content', '')
                if role in ('user', 'assistant') and content:
                    messages.append({'role': role, 'content': content})

        messages.append({'role': 'user', 'content': message.strip()})

        # Limit conversation context to last 20 messages to manage token usage
        if len(messages) > 20:
            messages = messages[-20:]

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=2048,
                system=system_prompt,
                messages=messages,
            )
            reply = response.content[0].text.strip()
            return reply, None

        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during chat')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during chat: {e}')
            return None, 'An error occurred while generating a response. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during chat: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    # ------------------------------------------------------------------
    # AI Search
    # ------------------------------------------------------------------

    @classmethod
    def search(cls, query):
        """
        Generate an AI-synthesized answer for a search query, including
        structured source-like references.

        Args:
            query: The user's search query string.

        Returns:
            Tuple of (result_dict, error).
            result_dict has keys: answer (str), sources (list of dicts with title, snippet).
        """
        system_prompt = (
            'You are an AI-powered research assistant on WritingBot.ai. '
            'Given a user query, provide a comprehensive, well-researched answer. '
            'Write the answer in clear, readable prose using markdown formatting '
            '(headings, bullet points, bold text, etc.). '
            'At the end, include a JSON block with synthesized source references. '
            'Return your response in this exact format:\n\n'
            'ANSWER:\n<your detailed answer in markdown>\n\n'
            'SOURCES_JSON:\n[{"title": "Source Title", "snippet": "Brief description of what this source covers"}]\n\n'
            'Include 3-5 relevant source references. The sources should be plausible, '
            'topic-relevant references that support the answer. '
            'Make the answer thorough (3-6 paragraphs) and informative.'
        )

        if not query or not query.strip():
            return None, 'Please enter a search query.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=3000,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': f'Research this topic: {query.strip()}'}
                ]
            )
            raw = response.content[0].text.strip()

            # Parse the structured response
            answer = raw
            sources = []

            if 'SOURCES_JSON:' in raw:
                parts = raw.split('SOURCES_JSON:', 1)
                answer = parts[0].strip()
                # Remove "ANSWER:" prefix if present
                if answer.startswith('ANSWER:'):
                    answer = answer[len('ANSWER:'):].strip()

                sources_raw = parts[1].strip()
                # Strip markdown code fences if present
                if sources_raw.startswith('```'):
                    sources_raw = sources_raw.split('\n', 1)[-1].rsplit('```', 1)[0].strip()
                try:
                    sources = json.loads(sources_raw)
                except json.JSONDecodeError:
                    logger.warning('Failed to parse AI search sources JSON')
                    sources = []
            elif 'ANSWER:' in raw:
                answer = raw.split('ANSWER:', 1)[1].strip()

            return {'answer': answer, 'sources': sources}, None

        except anthropic.RateLimitError:
            logger.warning('Anthropic rate limit reached during search')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error during search: {e}')
            return None, 'An error occurred while researching your query. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error during search: {e}')
            return None, 'An unexpected error occurred. Please try again.'
