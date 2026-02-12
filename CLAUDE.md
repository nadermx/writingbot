# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WritingBot.ai** is an AI-powered writing assistant platform competing with QuillBot.com. Built on Django 6.x (forked from nadermx/djangobase). Live at https://writingbot.ai.

**Server:** 38.248.6.212 (VPS.org, Ubuntu 24.04). Deploy path: `/home/www/writingbot/`

**DNS:** Managed via VPS.org API (`~/.credentials/vps_org_api_key`). Zone UUID: `6b025f8a-88fa-472a-85c0-9510239ab05e`. API base: `https://admin.vps.org/api/v1/dns-zones/{uuid}/records/` with Bearer token auth.

## Commands

```bash
# Development
cp config_example.py config.py   # First time only (gitignored)
pip install -r requirements.txt
python manage.py migrate
python manage.py set_languages   # Needs translations/json/languages.json
python manage.py runserver

# Tests (17 files, 230+ tests)
python manage.py test                    # Run all
python manage.py test tests.test_paraphraser  # Single test file
python manage.py test tests.test_pages   # All URL smoke tests
python manage.py test tests.test_api_endpoints  # API integration tests (uses REAL backends)
python manage.py test tests.test_user_flow  # User signup/login/credits tests
pytest tests/test_e2e.py                 # Playwright browser tests (requires: playwright install chromium)

# Seed content
python manage.py seed_blog    # 31 blog posts (--clear to reset)
python manage.py seed_courses # 15 courses, 57 chapters (--clear to reset)

# Other management commands
python manage.py set_plans            # Initialize payment plans
python manage.py rebill               # Daily subscription rebilling (cron: 6am)
python manage.py expire_pro_users     # Expire lapsed pro users (cron: 6:30am)
python manage.py run_translation      # Translate text bases (needs Google API key)

# Deployment
cd ansible
ansible-playbook -i servers gitpull.yml
# Run management commands on server:
ansible -i servers all -m shell -a "cd /home/www/writingbot && venv/bin/python manage.py <command>" --become --become-user=writingbot
```

## Architecture

### Apps Overview

**20+ Django apps.** Infrastructure: `core`, `accounts`, `translations`, `finances`, `contact_messages`, `api`. Writing tools: `paraphraser`, `grammar`, `summarizer`, `ai_detector`, `humanizer`, `plagiarism`, `translator`, `citations`, `flow`, `word_counter`. Content/SEO: `ai_tools` (98 generators), `media_tools` (27 image prompt generators), `pdf_tools`, `converter` (150+ format pairs), `seo`, `blog`, `courses`.

### URL Routing (`app/urls.py`)

Tool app URL includes come before `core` (catch-all) — **order matters**. When adding new apps, include them before the `core` line. Custom 404/500 handlers in `core.views`.

### LLMClient — Central AI Routing (`core/llm_client.py`)

All AI calls go through a single class:
```python
LLMClient.generate(system_prompt, messages, max_tokens=4096,
                   temperature=0.7, use_premium=False) -> (str, Optional[str])
LLMClient.detect_ai_text(text) -> (dict, Optional[str])
```
- `use_premium=False` → Qwen 2.5 14B via `https://api.writingbot.ai/v1/text/generate/` (GPU server at 38.248.6.142)
- `use_premium=True` → Claude API via Anthropic SDK
- `detect_ai_text()` → DeBERTa classifier via `/v1/text/ai-detect-model/` — returns `({"score": 72.5, "label": "ai", "chunks": [...]}, None)`
- Returns `(text, None)` on success, `(None, "error message")` on failure
- `extract_json()` helper in same file robustly parses JSON from LLM responses (strips preamble, markdown fences)

### Service Pattern — `(result, error)` Tuples

Every app has a `services.py` (17 total) returning 2-tuples. Success: `(result, None)`. Failure: `(None, "User-facing message")`. Services never raise exceptions to views.

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

`GlobalVars` lives in `accounts/views.py`. Every view calls `GlobalVars.get_globals(request)` which returns a dict with i18n strings, project settings, language info, and currency. **This requires a `Language` record with iso='en' in the database** — without it, views crash. Not a Django context processor; must be called manually in each view.

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
- `GENERATOR_REGISTRY` dict in `registry.py` (~1200 lines) maps slug → generator instance
- Single API endpoint `/api/ai-tools/generate/` serves all generators
- View reads slug from URL, looks up generator, renders shared `generator.html` template
- Generator category files: `academic.py`, `business.py`, `marketing.py`, `content.py`, `creative.py`, `professional.py`, `social_media.py`, `utility.py`

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
A generic view class with a `page_key` attribute renders the shared template. Converter pages auto-generate features/FAQs from format pair dicts (150+ combinations). Translator has three page types: main index, language page (`/translate/spanish/`), and pair page (`/translate/english-to-spanish/`).

### Converter Architecture (`converter/views.py`)

Format registries (`IMAGE_FORMATS`, `DOCUMENT_FORMATS`) drive auto-generated pairs. Cross-document conversions (e.g., Word→Excel) route through PDF as intermediate format. Dynamic content generators produce features, FAQs, and how-to steps per pair. API routing maps pairs to `/api/media/convert-image/` or `/api/pdf/convert/`.

### Public API (`api/`)

REST API at `/api/v1/` with `APIKeyAuthentication` (Bearer token from `CustomUser.api_token`). Endpoints: `/api/v1/paraphrase/`, `/api/v1/grammar/`, `/api/v1/summarize/`, `/api/v1/ai-detect/`, `/api/v1/translate/`. Custom throttling per plan. API docs at `/api/docs/`.

### Frontend Stack

- **Bootstrap 5.3** (CDN) + custom `static/css/styles.css` (single CSS file, no preprocessor)
- **Alpine.js** (CDN) for all interactive components — each tool has a JS file in `static/js/` returning an Alpine data function
- No build step. JS files versioned via `?v={{ g.scripts_version }}` query param
- CSRF token via `document.querySelector('[name=csrfmiddlewaretoken]')` or `meta[name="csrf-token"]`
- Base template (`templates/base.html`) has navbar with 4 dropdown menus, footer, auth buttons, language switcher
- Frontend error logging: JS errors POST to `/api/accounts/log-error/`

### Configuration

- `config.py` (gitignored) — secrets, API keys, DB credentials. Copy from `config_example.py`
- `app/settings.py` — imports `config.py` via `from config import *`, defines `TOOL_LIMITS` dict for free tier limits
- Key settings: `ANTHROPIC_API_KEY`, `WRITINGBOT_API_KEY`
- `TOOL_LIMITS` dict defines per-tool free tier constraints (word counts, daily limits). When adding a new tool, add its limits here.
- Redis DB 0 for Django-RQ job queues (`default`, `high`, `low`), DB 1 for general cache, DB 2 for select2 widget cache. Sessions also in Redis.

### Translation System

Custom i18n (NOT Django's built-in). `Language` and `Translation` models in `translations/` app. `GlobalVars.get_globals()` fetches i18n dict for current language. Languages cached in Redis. Templates use `{{ g.i18n.code_name|default:"Fallback" }}`.

## Testing

Tests mock `core.llm_client.LLMClient.generate` via `@patch`. Mock responses defined in `tests/conftest.py` — the `mock_llm_generate` function dispatches based on keywords in `system_prompt` (e.g., 'paraphras' → paraphrase response, 'grammar' → grammar response). When adding a new service that calls `LLMClient`, add a matching keyword branch in `mock_llm_generate`. AI detector tests mock `LLMClient.detect_ai_text` (not `generate`) since it uses the DeBERTa endpoint directly.

Every test class needs `Language.objects.create(name='English', iso='en')` in `setUpTestData` for `GlobalVars` to work. DRF throttle can cause 429s across test suites — clear via `SimpleRateThrottle.cache.clear()` in `setUp`.

```python
from tests.conftest import mock_llm_generate

@patch('core.llm_client.LLMClient.generate', side_effect=mock_llm_generate)
class MyServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='English', iso='en', active=True, default=True)
```

## Conventions

- User-facing tool URLs are hyphenated: `/ai-content-detector/`, `/grammar-checker/`
- Commit messages: short imperative subject lines starting with `Fix`, `Add`, `Update`, or `Refactor`
- App structure: `models.py`, `views.py`, `services.py`, `urls.py` per app
- Test files: `tests/test_<feature>.py`

## Known Pitfalls

- **Django `APPEND_SLASH`** redirects POST→GET (301) — always use trailing slashes in API URLs
- **pypdf** `compress_content_streams()` must be called AFTER `add_page()`, not before
- **Alpine.js `x-show`** elements flash on load — use `x-cloak` attribute
- **`w-sm-auto`** is NOT a valid Bootstrap 5 class
- **DRF throttle** causes 429s across test suites — clear cache in `setUp`

## Deployment Notes

- Migrations are gitignored — run `makemigrations <app_name>` on server (specify app names explicitly)
- After deploy, `collectstatic` runs automatically via `gitpull.yml`
- `gitpull.yml` does NOT update nginx — deploy nginx config separately: `ansible -i servers all -m template -a "src=files/nginx.conf.j2 dest=/etc/nginx/sites-available/writingbot.conf mode=0644" --become` then `ansible -i servers all -m shell -a "nginx -t && systemctl reload nginx" --become`
- Restart app: `supervisorctl restart writingbot`
- Logs: `/var/log/writingbot/writingbot.err.log` (Gunicorn startup only; runtime errors need `DEBUG=True` or test via RequestFactory)
- DB user needs `CREATEDB` permission for running tests: `ALTER USER writingbot CREATEDB;`
- **Nginx template gotcha:** `ansible/files/nginx.conf.j2` is processed by Ansible's Jinja2 engine. Any nginx `set`, `if`, or `$variable` directives that conflict with Jinja2 must be wrapped in `{% raw %}...{% endraw %}` blocks (see the Clicky proxy section for an example).
