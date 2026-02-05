# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DjangoBase is a reusable Django 5.x project template with built-in user authentication, credits-based billing, multi-processor payments (Stripe, PayPal, Square, Coinbase), and a custom database-driven translation system. It's designed to be cloned and customized for new SaaS projects.

## Common Commands

```bash
# Development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser

# Translations
python manage.py set_languages      # Load languages from JSON
python manage.py run_translation    # Auto-translate via Google Translate API

# Plans
python manage.py set_plans          # Load plans from finances/json/plans.json

# PayPal Setup (if using subscriptions)
python manage.py create_paypal_product
python manage.py create_paypal_plans

# Subscription Management (run via cron)
python manage.py rebill             # Daily billing for subscriptions
python manage.py expire_pro_users   # Deactivate expired subscriptions

# Run tests
python manage.py test
python manage.py test accounts      # Single app
```

## Quick Start for New Projects

```bash
python customize.py           # Interactive setup script
cp config_example.py config.py  # If not using customize.py
pip install -r requirements.txt
python manage.py migrate
python manage.py set_languages
python manage.py runserver
```

See `SETUP.md` for detailed customization instructions.

## Architecture

### Configuration
Settings split between `app/settings.py` (Django defaults) and `config.py` (secrets/env-specific). The `config.py` is gitignored - copy from `config_example.py` or use `customize.py`.

Key config values:
- `PROJECT_NAME` - Used in templates, emails, and payment descriptions
- `PROJECT_DOMAIN` - Your domain for email sending
- `ROOT_DOMAIN` - Full URL (e.g., https://myapp.com)
- `SECRET_KEY` - Django secret key (generate a unique one for production)
- `CSRF_TRUSTED_ORIGINS` - Required for Django 4+ to fix 403 errors
- `ALLOWED_HOSTS` - List of allowed hostnames
- `CURRENCY_CODE` - Currency code (default: 'USD')
- `CURRENCY_SYMBOL` - Currency symbol (default: '$')
- `PROCESSORS` - List of enabled payment processors: `['stripe', 'paypal']`

### Custom Translation System
**Not Django's built-in i18n.** Uses three models in `translations/`:
- `Language` - available languages (populated via `set_languages` command)
- `TextBase` - source text entries with `code_name` identifier
- `Translation` - translated text per language

Usage in views: `Translation.get_text_by_lang('en')` returns dict of `{code_name: text}`. Add new text via admin at `Translations > Text bases`, then run `python manage.py run_translation`.

### User & Authentication
Custom user model `accounts.CustomUser` (single file at `accounts/models.py`) with:
- Email as username (`USERNAME_FIELD = "email"`)
- Credits system for usage-based billing
- Subscription tracking (`is_plan_active`, `next_billing_date`, `plan_subscribed`)
- Payment processor tokens (`payment_nonce`, `card_nonce`, `processor`)
- 6-digit email verification codes (`verification_code`)
- API token for external authentication

User model contains most business logic as static methods: `register_user()`, `login_user()`, `upgrade_account()`, `cancel_subscription()`, etc.

### Email System
Uses `Utils.send_email()` from `app/utils.py` with Django's native SMTP backend. See `EMAIL_SETUP.md` for DNS configuration.

Email templates in `templates/mailing/` use `{{ project_name }}`, `{{ root_domain }}`, and `{{ currency_symbol }}` variables.

For development, set in `config.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Payment Processing
`finances/` supports Stripe, Square, PayPal, Coinbase. Plans defined in `finances/json/plans.json` or admin.

Key models:
- `Plan` (`finances/models/plan.py`) - pricing, credits granted, subscription length, processor keys
- `Payment` (`finances/models/payment.py`) - transactions with status (pending/success/failed/refunded)

Payment methods are static on `Payment`: `make_charge_stripe()`, `make_charge_square()`, `make_charge_paypal()`.

Webhooks at `/ipns/paypal` and `/ipns/coinbase`.

### View Pattern
All views call `GlobalVars.get_globals(request)` from `accounts/views.py` to build context:
```python
settings = GlobalVars.get_globals(request)
# Returns: {
#   'lang': Language,
#   'i18n': {code_name: text},
#   'languages': [...],
#   'scripts_version': str,
#   'project_name': str,
#   'currency_symbol': str,
#   'currency_code': str
# }
```
Templates receive this as `g` context variable (e.g., `{{ g.i18n.welcome_title }}`, `{{ g.currency_symbol }}`).

Views are class-based in `core/views.py`. Most authentication/payment logic is delegated to `CustomUser` model methods.

### API Endpoints
REST Framework views in `accounts/views.py` (not a separate api_views.py):
- `/api/accounts/rate_limit/` - Check usage quotas per IP
- `/api/accounts/consume/` - Decrement credits after API usage
- `/api/accounts/resend-verification/` - Resend email verification
- `/api/accounts/cancel-subscription/` - Cancel active subscription
- `/api/accounts/log-error/` - Log frontend JavaScript errors

### Frontend
- Bootstrap 5.3 (loaded via CDN)
- Custom styles in `static/css/styles.css`
- Language selector in navbar with `?lang=` URL parameter
- All templates use consistent card-based layout


## Key Patterns

### Method Return Convention
Methods return `(object, error)` tuples - check first element for success:
```python
payment, errors = Payment.make_charge_stripe(user, token, amount, settings)
if errors:
    # handle error
```
This pattern is used throughout: `CustomUser.register_user()`, `Payment.make_refund()`, `Message.save_message()`, etc.

### Template Variables
All templates have access to the `g` context with:
- `g.i18n.{code_name}` - Translated text (use `|default:"Fallback"` for safety)
- `g.project_name` - Project name from config
- `g.currency_symbol` - Currency symbol ($, €, etc.)
- `g.currency_code` - Currency code (USD, EUR, etc.)
- `g.lang` - Current language object
- `g.languages` - All available languages
- `g.scripts_version` - For cache busting

### Adding New Translations
1. Add TextBase entry in admin (`Translations > Text bases`) with unique `code_name`
2. Run `python manage.py run_translation` to auto-translate via Google API
3. Access in templates: `{{ g.i18n.your_code_name|default:"Fallback" }}`

### Rate Limiting
- API rate limiting in `RateLimit` view uses IP+User-Agent hash stored in Redis
- Payment rate limiting in `CustomUser.payment_ratelimited()` - max 3 attempts per hour
- Authenticated users with active plans or credits bypass limits

### Caching
Uses Django-Redis. Cache helpers in `app/utils.py`:
- `Utils.get_from_cache(key)` / `Utils.set_to_cache(key, value, exp)`
- Languages are cached globally in `GlobalVars.get_globals()`

### Logging
Uses StreamHandler (logs to stderr) so supervisor captures all output automatically.

**Backend Logging:**
```python
import logging
logger = logging.getLogger('app')
logger.warning('Something happened')
logger.error('Something failed', exc_info=True)
```

Logs appear in supervisor's stderr file: `/var/log/{project}/{project}.err.log`

**Frontend Error Logging:**
JavaScript errors are automatically captured via `window.onerror` and `unhandledrejection` handlers in `base.html`. Errors are POSTed to `/api/accounts/log-error/` and logged with the `app` logger.

Frontend error logs include: message, source file, line/column, stack trace, URL, user ID, and user agent.

**View logs on server:**
```bash
ansible -i servers all -m shell -a "tail -100 /var/log/{project}/{project}.err.log" --become
```

## Deployment

Ansible playbooks in `ansible/` for Ubuntu 24.04.

### IMPORTANT: Two-Step Initial Deployment

**You MUST run `disableroot.yml` first on a new server.** This creates the deploy user and disables root SSH access for security.

### First Deployment (New Server)

```bash
cd ansible

# 1. Copy and configure files
cp servers.example servers                    # Add server IP
cp group_vars/all.example group_vars/all      # Add credentials

# 2. Add your SSH key to root
ssh-copy-id root@your-server-ip

# 3. REQUIRED: Create deploy user and disable root (run ONCE)
ansible-playbook -i servers disableroot.yml -e "ansible_user=root"

# 4. Deploy application
ansible-playbook -i servers djangodeployubuntu24.yml --tags=all,first_run
```

> **After step 3, root SSH is DISABLED.** All future access uses the deploy user.

### Subsequent Deployments

```bash
ansible-playbook -i servers gitpull.yml              # Quick code update
ansible-playbook -i servers djangodeployubuntu24.yml  # Full redeploy
```

### Required Variables in `group_vars/all`

| Variable | Description |
|----------|-------------|
| `deploy_user` | Non-root user that runs the app |
| `deploy_password` | Password for deploy user |
| `db_name`, `db_user`, `db_password` | PostgreSQL credentials |
| `githuburl` | Repository URL |
| `projectname` | Used for nginx/supervisor configs |
| `domain` | Your domain name |
