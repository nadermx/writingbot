"""
Base AI Service Layer for WritingBot.ai
Handles all communication with AI providers (Claude API).
"""
import json
import logging
from django.conf import settings

logger = logging.getLogger('app')


class AIService:
    """Base class for all AI-powered tool services."""

    PROVIDER_CLAUDE = 'claude'

    @staticmethod
    def get_client():
        """Get Anthropic client instance."""
        try:
            import anthropic
            return anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {e}")
            raise

    @staticmethod
    def call_claude(system_prompt, user_message, max_tokens=4096, temperature=0.7, json_mode=False):
        """
        Make a call to Claude API.

        Args:
            system_prompt: System instructions for Claude
            user_message: The user's input text
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0-1.0)
            json_mode: If True, instruct Claude to return valid JSON

        Returns:
            str: Claude's response text

        Raises:
            Exception: If API call fails
        """
        client = AIService.get_client()
        model = getattr(settings, 'ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')

        if json_mode:
            system_prompt += "\n\nIMPORTANT: You must respond with valid JSON only. No markdown, no code blocks, no explanation outside the JSON."

        try:
            message = client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ],
                temperature=temperature,
            )
            response_text = message.content[0].text

            if json_mode:
                # Strip markdown code blocks if present
                response_text = response_text.strip()
                if response_text.startswith('```'):
                    lines = response_text.split('\n')
                    # Remove first and last lines (```json and ```)
                    lines = [l for l in lines if not l.strip().startswith('```')]
                    response_text = '\n'.join(lines)

            return response_text

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise

    @staticmethod
    def call_claude_json(system_prompt, user_message, max_tokens=4096, temperature=0.7):
        """
        Call Claude and parse response as JSON.

        Returns:
            dict: Parsed JSON response
        """
        response = AIService.call_claude(
            system_prompt, user_message, max_tokens, temperature, json_mode=True
        )
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse Claude JSON response: {response[:200]}")
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            raise

    @staticmethod
    def count_words(text):
        """Count words in text."""
        if not text:
            return 0
        return len(text.split())

    @staticmethod
    def count_chars(text):
        """Count characters in text."""
        if not text:
            return 0
        return len(text)

    @staticmethod
    def check_word_limit(text, limit):
        """Check if text exceeds word limit. Returns (is_within_limit, word_count)."""
        word_count = AIService.count_words(text)
        return word_count <= limit, word_count

    @staticmethod
    def check_char_limit(text, limit):
        """Check if text exceeds character limit. Returns (is_within_limit, char_count)."""
        char_count = AIService.count_chars(text)
        return char_count <= limit, char_count

    @staticmethod
    def is_premium_user(user):
        """Check if user has an active premium subscription."""
        if not user or not user.is_authenticated:
            return False
        return getattr(user, 'is_plan_active', False)

    @staticmethod
    def get_tool_limit(tool_name, key, user=None):
        """Get the appropriate limit for a tool based on user's plan."""
        limits = getattr(settings, 'TOOL_LIMITS', {}).get(tool_name, {})
        if user and AIService.is_premium_user(user):
            # Premium users get premium limits or no limit
            premium_key = f'premium_{key.replace("free_", "")}'
            return limits.get(premium_key, None)  # None = unlimited
        return limits.get(key, None)
