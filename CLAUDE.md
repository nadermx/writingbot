# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WritingBot.ai** is an AI-powered writing assistant platform competing with QuillBot.com. Built on Django 6.x (forked from nadermx/djangobase). Live at https://writingbot.ai.

**Server:** 38.248.6.212 (VPS.org, Ubuntu 24.04). Deploy path: `/home/www/writingbot/`

## Commands

```bash
# Development
cp config_example.py config.py   # First time only (gitignored)
pip install -r requirements.txt
python manage.py migrate
python manage.py set_languages   # Needs translations/json/languages.json
python manage.py runserver

# Tests (14 files, 131+ tests)
python manage.py test                    # Run all
python manage.py test tests.test_paraphraser  # Single test file
python manage.py test tests.test_pages   # All URL smoke tests

# Seed content
python manage.py seed_blog    # 31 blog posts (--clear to reset)
python manage.py seed_courses # 15 courses, 57 chapters (--clear to reset)

# Deployment
cd ansible
ansible-playbook -i servers gitpull.yml
# Run management commands on server:
ansible -i servers all -m shell -a "cd /home/www/writingbot && venv/bin/python manage.py <command>" --become --become-user=writingbot
```

## Architecture

### LLMClient — Central AI Routing (`core/llm_client.py`)

All AI calls go through a single class:
```python
LLMClient.generate(system_prompt, messages, max_tokens=4096,
                   temperature=0.7, use_premium=False) -> (str, Optional[str])
```
- `use_premium=False` → Mistral 7B via `https://api.writingbot.ai/v1/text/generate/` (GPU server at 38.248.6.142)
- `use_premium=True` → Claude API via Anthropic SDK
- Returns `(text, None)` on success, `(None, "error message")` on failure

### Service Pattern — `(result, error)` Tuples

Every app has a `services.py` that returns 2-tuples. Success: `(result, None)`. Failure: `(None, "User-facing message")`.

```python
# Paraphraser
AIParaphraseService.paraphrase(text, mode='standard', synonym_level=3,
    frozen_words=None, language='en', use_premium=False) -> (str, error)

# Grammar (returns dict with corrections, writing_scores, tone)
AIGrammarService().check_grammar(text, dialect='en-us', use_premium=False) -> (dict, error)

# AI Tools (rate-limited: 50/day free)
AIToolsService.generate(slug, params, user, ip, user_agent) -> (str, error)
```

### View Pattern — GlobalVars Context

Every view calls `GlobalVars.get_globals(request)` which returns a dict with i18n strings, project settings, language info, and currency. This requires a `Language` record with iso='en' in the database.

```python
class SomePage(View):
    def get(self, request):
        g = GlobalVars.get_globals(request)
        return render(request, 'template.html', {
            'title': f'Page Title | {config.PROJECT_NAME}',
            'description': 'Meta description',
            'page': 'page-name',
            'g': g,
        })
```

### AI Tools Generator Framework (`ai_tools/generators/`)

98 generators across 11 categories share a `BaseGenerator` pattern:
- Each generator defines `slug`, `name`, `category`, `fields` (form schema), and `system_prompt` (with `{field_name}` placeholders)
- `GENERATOR_REGISTRY` dict maps slug → generator instance
- Single API endpoint `/api/ai-tools/generate/` serves all generators
- View reads slug from URL, looks up generator, renders shared `generator.html` template

### SEO Landing Pages Pattern

Dictionary-driven content pages used by `seo/`, `translator/`, `converter/` apps:
```python
SEO_PAGES = {
    'page-slug': {
        'h1': 'Title', 'subtitle': '...', 'meta_title': '...', 'meta_description': '...',
        'features': [{'title': '...', 'text': '...'}],
        'faqs': [{'q': '...', 'a': '...'}],
    }
}
```
A generic view class with a `page_key` attribute renders the shared template. Converter pages auto-generate content from format pair dicts (150+ combinations).

### Frontend Stack

- **Bootstrap 5.3** (CDN) + custom `static/css/styles.css`
- **Alpine.js** (CDN) for all interactive components — each tool has a JS file returning an Alpine data function
- No build step. JS files versioned via `?v={{ g.scripts_version }}` query param
- CSRF token via `document.querySelector('[name=csrfmiddlewaretoken]')` or `meta[name="csrf-token"]`

### Configuration

- `config.py` (gitignored) — secrets, API keys, DB credentials. Copy from `config_example.py`
- `app/settings.py` — imports `config.py`, defines `TOOL_LIMITS` dict for free tier limits
- Key settings: `ANTHROPIC_API_KEY`, `WRITINGBOT_API_KEY`, `TRANSLATEAPI_KEY`

## Testing

Tests mock `core.llm_client.LLMClient.generate` via `@patch`. Mock responses defined in `tests/conftest.py`. Every test class needs `Language.objects.create(name='English', iso='en')` in `setUpTestData` for `GlobalVars` to work.

```python
from tests.conftest import mock_llm_generate

@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class MyServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='English', iso='en', active=True, default=True)
```

## Deployment Notes

- Migrations are gitignored — run `makemigrations <app_name>` on server (specify app names explicitly)
- After deploy, `collectstatic` runs automatically via `gitpull.yml`
- Restart: `supervisorctl restart writingbot`
- Logs: `/var/log/writingbot/writingbot.err.log` (Gunicorn startup only; runtime errors need `DEBUG=True` or test via RequestFactory)
- DB user needs `CREATEDB` permission for running tests: `ALTER USER writingbot CREATEDB;`
