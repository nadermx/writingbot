import json
import logging
import re

import requests
from django.conf import settings

logger = logging.getLogger('app')


def extract_json(text):
    """
    Robustly extract a JSON object from LLM output that may contain
    preamble text, markdown code fences, or trailing commentary.

    Returns parsed dict/list on success, raises ValueError on failure.
    """
    if not text or not text.strip():
        raise ValueError('Empty response')

    s = text.strip()

    # 1. Strip markdown code fences (```json ... ``` or ``` ... ```)
    fence_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)```', s)
    if fence_match:
        s = fence_match.group(1).strip()

    # 2. Try parsing directly
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        pass

    # 3. Find the outermost { ... } or [ ... ] in the text
    for open_ch, close_ch in [('{', '}'), ('[', ']')]:
        start = s.find(open_ch)
        if start == -1:
            continue
        depth = 0
        in_string = False
        escape = False
        end = -1
        for i in range(start, len(s)):
            c = s[i]
            if escape:
                escape = False
                continue
            if c == '\\' and in_string:
                escape = True
                continue
            if c == '"' and not escape:
                in_string = not in_string
                continue
            if in_string:
                continue
            if c == open_ch:
                depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0:
                    end = i
                    break
        if end != -1:
            try:
                return json.loads(s[start:end + 1])
            except json.JSONDecodeError:
                pass

    raise ValueError(f'No valid JSON found in response: {text[:200]}')


class LLMClient:
    """
    Unified LLM client that routes to either the open-source model
    (via api.writingbot.ai / ollama) or Claude (for premium users).

    All methods return (text, error) tuples matching existing service patterns.
    """

    @classmethod
    def generate(cls, system_prompt, messages, max_tokens=4096,
                 temperature=0.7, use_premium=False):
        """
        Generate text using either open-source LLM or Claude.

        Args:
            system_prompt: System instruction string.
            messages: List of dicts with 'role' and 'content'.
            max_tokens: Maximum tokens to generate.
            temperature: Sampling temperature.
            use_premium: If True and Claude API key is set, use Claude.

        Returns:
            Tuple of (text, error). On success error is None.
        """
        if use_premium and getattr(settings, 'ANTHROPIC_API_KEY', ''):
            return cls._call_claude(system_prompt, messages, max_tokens, temperature)
        return cls._call_open_source(system_prompt, messages, max_tokens, temperature)

    @classmethod
    def detect_ai_text(cls, text):
        """
        Detect AI-generated text using the DeBERTa classifier on the GPU server.

        Args:
            text: Text to analyze.

        Returns:
            Tuple of (dict, error). Dict has 'score', 'label', 'chunks'.
        """
        api_url = getattr(settings, 'WRITINGBOT_API_URL', '')
        api_key = getattr(settings, 'WRITINGBOT_API_KEY', '')

        if not api_url:
            return None, 'AI detection service is not configured.'

        try:
            resp = requests.post(
                f'{api_url.rstrip("/")}/v1/text/ai-detect-model/',
                json={'text': text},
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=120,
            )

            if resp.status_code != 200:
                error_data = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', f'AI detection service returned {resp.status_code}')
                logger.error(f'AI detect model error: {resp.status_code} - {error_msg}')
                return None, 'AI detection service is temporarily unavailable. Please try again.'

            return resp.json(), None

        except requests.exceptions.Timeout:
            logger.error('AI detect model request timed out')
            return None, 'The request timed out. Please try again.'
        except requests.exceptions.ConnectionError:
            logger.error('Cannot connect to AI detect model service')
            return None, 'AI detection service is temporarily unavailable. Please try again.'
        except Exception as e:
            logger.error(f'AI detect model unexpected error: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    @classmethod
    def _call_open_source(cls, system_prompt, messages, max_tokens, temperature):
        """Call the open-source LLM via api.writingbot.ai."""
        api_url = getattr(settings, 'WRITINGBOT_API_URL', '')
        api_key = getattr(settings, 'WRITINGBOT_API_KEY', '')

        if not api_url:
            return None, 'LLM service is not configured.'

        try:
            resp = requests.post(
                f'{api_url.rstrip("/")}/v1/text/generate/',
                json={
                    'system_prompt': system_prompt,
                    'messages': messages,
                    'max_tokens': max_tokens,
                    'temperature': temperature,
                },
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json',
                },
                timeout=120,
            )

            if resp.status_code != 200:
                error_data = resp.json() if resp.headers.get('content-type', '').startswith('application/json') else {}
                error_msg = error_data.get('error', f'LLM service returned {resp.status_code}')
                logger.error(f'Open-source LLM error: {resp.status_code} - {error_msg}')
                return None, 'An error occurred while generating text. Please try again.'

            data = resp.json()
            text = data.get('text', '')
            if not text:
                return None, 'Empty response from LLM service.'
            return text, None

        except requests.exceptions.Timeout:
            logger.error('Open-source LLM request timed out')
            return None, 'The request timed out. Please try again.'
        except requests.exceptions.ConnectionError:
            logger.error('Cannot connect to open-source LLM service')
            return None, 'AI service is temporarily unavailable. Please try again.'
        except Exception as e:
            logger.error(f'Open-source LLM unexpected error: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    @classmethod
    def _call_claude(cls, system_prompt, messages, max_tokens, temperature):
        """Call Claude API (Anthropic) for premium users."""
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=getattr(settings, 'ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929'),
                max_tokens=max_tokens,
                system=system_prompt,
                messages=messages,
            )
            text = response.content[0].text.strip()
            return text, None

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f'Claude API error ({error_type}): {e}')

            # Try to give user-friendly errors
            if 'RateLimitError' in error_type:
                return None, 'Service is temporarily busy. Please try again in a moment.'
            if 'AuthenticationError' in error_type:
                return None, 'AI service configuration error. Please contact support.'

            return None, 'An error occurred while generating text. Please try again.'
