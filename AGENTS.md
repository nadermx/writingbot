# Repository Guidelines

## Project Structure & Module Organization
This is a Django 6 monorepo centered on writing tools.
- `app/`: Django settings, root URL config, ASGI/WSGI.
- Feature apps: `paraphraser/`, `grammar/`, `summarizer/`, `translator/`, `ai_detector/`, `flow/`, `media_tools/`, `pdf_tools/`, `ai_tools/`, etc.
- Platform apps: `accounts/`, `api/`, `finances/`, `translations/`, `core/`, `contact_messages/`.
- Frontend assets: `templates/`, `static/css/`, `static/js/`.
- Tests: `tests/` (integration + service + e2e smoke tests).
- Ops/deploy: `ansible/`.

## Build, Test, and Development Commands
- `cp config_example.py config.py`: create local config (required first step).
- `pip install -r requirements.txt`: install dependencies.
- `python manage.py migrate && python manage.py set_languages`: initialize DB and language records.
- `python manage.py runserver`: start local server at `http://localhost:8000`.
- `python manage.py test`: run Django test suite.
- `python manage.py test tests.test_paraphraser`: run a targeted test module.
- `pytest tests/test_e2e.py`: run Playwright browser tests (install browser first: `playwright install chromium`).

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation.
- Keep app structure consistent: `models.py`, `views.py`, `services.py`, `urls.py`.
- Use snake_case for Python names and test files (`tests/test_<feature>.py`).
- Keep user-facing tool URLs hyphenated (example: `/ai-content-detector/`).
- Put shared frontend logic in `static/js/<tool>.js`; keep template names aligned with feature paths.

## Testing Guidelines
- Add tests in `tests/`, grouped by feature/service.
- Name tests by behavior (example: `test_page_loads_without_console_errors`).
- Mock LLM calls with `tests.conftest.mock_llm_generate` when testing AI-dependent services.
- Ensure required baseline data (notably `Language(iso='en')`) exists in test setup for pages using global context.

## Commit & Pull Request Guidelines
- Follow existing commit style: short imperative subject lines, typically starting with `Fix`, `Add`, `Update`, or `Refactor`.
- Keep commits focused to one logical change.
- PRs should include:
  - concise summary of behavior changes,
  - test evidence (`python manage.py test ...` / `pytest ...`),
  - screenshots for UI/template updates,
  - linked issue or task when applicable.

## Security & Configuration Tips
- Never commit secrets or environment-specific files (`config.py`, `ansible/servers`, `ansible/group_vars/all`).
- Treat migrations as deployment artifacts in this repo workflow; generate/apply them per environment as documented.
