# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**WritingBot.ai** is an AI-powered writing assistant platform competing with QuillBot.com. Built on Django 6.x (forked from nadermx/djangobase), it offers paraphrasing, grammar checking, AI detection, summarization, translation, citation generation, plagiarism checking, and 100+ AI writing tool generators.

**Domain:** writingbot.ai
**Repository:** https://github.com/nadermx/writingbot

## Common Commands

```bash
# Development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser

# Translations
python manage.py set_languages
python manage.py run_translation

# Plans
python manage.py set_plans

# Subscription Management (cron)
python manage.py rebill
python manage.py expire_pro_users

# Tests
python manage.py test
python manage.py test paraphraser
```

## Quick Start

```bash
cp config_example.py config.py   # Configure secrets
pip install -r requirements.txt
python manage.py migrate
python manage.py set_languages
python manage.py runserver
```

## Architecture

### Core Apps (from djangobase)
- `accounts/` - Custom user model (email-based auth, credits, subscriptions)
- `finances/` - Plans, payments (Stripe, PayPal, Square)
- `translations/` - Database-driven i18n system
- `contact_messages/` - Contact form
- `core/` - Static pages (about, terms, privacy, pricing, auth pages)

### Tool Apps (WritingBot-specific)
- `paraphraser/` - Flagship paraphrasing tool (10 modes, synonym slider, freeze words)
- `grammar/` - Grammar checker (spelling, punctuation, style, writing score)
- `summarizer/` - Text summarization (key sentences, paragraph, length slider)
- `ai_detector/` - AI content detection (sentence-level scoring)
- `humanizer/` - AI text humanizer (basic + advanced modes)
- `plagiarism/` - Plagiarism checker (premium only, web scanning)
- `translator/` - Translation tool (52+ languages)
- `citations/` - Citation generator (1000+ styles, autocite)
- `word_counter/` - Word/character counter
- `flow/` - Co-Writer workspace (document editor, research, AI suggestions)
- `ai_tools/` - 100+ AI writing generators (generic framework)
- `pdf_tools/` - PDF processing suite
- `media_tools/` - Image, audio, converter tools
- `courses/` - Free educational courses (OER)
- `blog/` - Content marketing blog
- `seo/` - SEO landing pages
- `api/` - Public API (v1)

### Configuration
- `app/settings.py` - Django settings
- `config.py` - Secrets, API keys (gitignored)
- `config_example.py` - Template for config.py

### Key Patterns
- Views use `GlobalVars.get_globals(request)` for context (i18n, settings)
- Templates access context via `{{ g.i18n.key }}`, `{{ g.project_name }}`
- Methods return `(result, error)` tuples
- AI services in each app's `services.py` handle LLM API calls
- Rate limiting uses IP+User-Agent hash in Redis
- All AI tools share a generic generator pattern in `ai_tools/generators/`

### AI Service Layer
- Primary: Claude API (Anthropic) for NLP tasks
- Translation: translateapi.ai
- All AI calls go through `services.py` in each app
- Rate limits enforced per tool, per user tier (free/premium)

### Frontend
- Tailwind CSS for styling
- Alpine.js for reactivity
- TipTap/ProseMirror for rich text editing (Flow)
- Vanilla JS for tool interactions
- No build step required for MVP

### Free vs Premium Limits
| Tool | Free | Premium |
|------|------|---------|
| Paraphraser | 500 words, 2 modes | Unlimited, all modes |
| Grammar | Basic | Advanced + rewrites |
| Summarizer | 1,200 words | 6,000 words |
| AI Detector | 1,200 words | Unlimited |
| Plagiarism | Not included | 30,000 words/mo |
| Translator | 5,000 chars | Unlimited |
| AI Tools | 50/day | Unlimited |

## Deployment

Uses Ansible (from djangobase):
```bash
cd ansible
ansible-playbook -i servers djangodeployubuntu24.yml --tags=all,first_run
ansible-playbook -i servers gitpull.yml
```

## Development Plan

See `DEVELOPMENT_PLAN.md` for the full competitive analysis, feature inventory, technical architecture, database schema, API design, and phased implementation roadmap.
