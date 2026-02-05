import logging

import anthropic
from django.conf import settings

logger = logging.getLogger('app')


class BaseGenerator:
    """
    Base class for all AI writing tool generators.

    Each generator defines its own slug, name, description, category,
    input fields, and system prompt. The generate() method builds a prompt
    from the user's inputs and calls the Claude API.
    """

    slug = ''
    name = ''
    description = ''
    category = ''
    icon = ''
    meta_title = ''
    meta_description = ''

    # List of field definitions for the input form.
    # Each field is a dict with keys:
    #   name, label, type (text|textarea|select|number), required, placeholder, options (for select)
    fields = []

    # The system prompt template. Use {field_name} placeholders that match field names.
    system_prompt = ''

    def get_prompt(self, params):
        """
        Format the system prompt with user-supplied parameters.

        Replaces {field_name} placeholders in the system_prompt with values
        from the params dict. Missing keys are replaced with empty strings.
        """
        prompt = self.system_prompt
        for field in self.fields:
            key = field['name']
            value = params.get(key, '')
            prompt = prompt.replace('{' + key + '}', str(value))
        # Also replace tone/style if present in params but not in fields
        for key in ('tone', 'style', 'language'):
            if '{' + key + '}' in prompt:
                prompt = prompt.replace('{' + key + '}', str(params.get(key, '')))
        return prompt

    def generate(self, params):
        """
        Build the prompt from params and call the Claude API.

        Args:
            params: dict of user input values keyed by field name.

        Returns:
            Tuple of (output_text, error). On success error is None.
        """
        system_prompt = self.get_prompt(params)

        # Build user message from all provided params
        user_parts = []
        for field in self.fields:
            key = field['name']
            value = params.get(key, '')
            if value:
                user_parts.append(f"{field['label']}: {value}")

        # Include tone if provided
        tone = params.get('tone', '')
        if tone:
            user_parts.append(f"Tone: {tone}")

        user_message = '\n'.join(user_parts) if user_parts else 'Generate content based on the system instructions.'

        try:
            client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            response = client.messages.create(
                model=settings.ANTHROPIC_MODEL,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {'role': 'user', 'content': user_message}
                ],
            )
            output_text = response.content[0].text
            return output_text, None

        except anthropic.RateLimitError:
            logger.warning(f'Anthropic rate limit reached for tool: {self.slug}')
            return None, 'Service is temporarily busy. Please try again in a moment.'
        except anthropic.APIError as e:
            logger.error(f'Anthropic API error for tool {self.slug}: {e}')
            return None, 'An error occurred while generating content. Please try again.'
        except Exception as e:
            logger.error(f'Unexpected error for tool {self.slug}: {e}')
            return None, 'An unexpected error occurred. Please try again.'

    def to_dict(self):
        """Serialize the generator config to a dict for templates and API responses."""
        return {
            'slug': self.slug,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'icon': self.icon,
            'meta_title': self.meta_title,
            'meta_description': self.meta_description,
            'fields': self.fields,
        }
