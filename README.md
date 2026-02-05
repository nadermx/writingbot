# DjangoBase

A minimal, reusable Django 5.x project template with:
- Custom user authentication (email-based)
- Credits-based billing system
- Multi-processor payments (Stripe, PayPal, Square, Coinbase)
- Database-driven translation system
- Native SMTP email (no third-party services)
- Bootstrap 5.3 frontend
- Redis caching and job queues

## Quick Start

```bash
# Clone and customize
git clone https://github.com/yourusername/djangobase.git myproject
cd myproject
python customize.py  # Interactive setup script

# Or manual setup
cp config_example.py config.py  # Edit with your settings

# Install dependencies
pip install -r requirements.txt

# Database
createdb myproject
python manage.py migrate
python manage.py set_languages
python manage.py createsuperuser

# Run
python manage.py runserver
```

## Configuration

Edit `config.py` with your settings (copy from `config_example.py`):

### Required Settings
| Setting | Description |
|---------|-------------|
| `PROJECT_NAME` | Your project name (used in emails, templates) |
| `PROJECT_DOMAIN` | Your domain (e.g., myproject.com) |
| `ROOT_DOMAIN` | Full URL (e.g., https://myproject.com) |
| `SECRET_KEY` | Django secret key - **generate a unique one for production** |
| `DEBUG` | Set to `False` in production |

### Django 4+ Requirements (Fixes 403 CSRF Errors)
| Setting | Description |
|---------|-------------|
| `CSRF_TRUSTED_ORIGINS` | **Required** - List of trusted domains with protocol |
| `ALLOWED_HOSTS` | List of allowed hostnames |

```python
# Example - add YOUR domains here:
CSRF_TRUSTED_ORIGINS = [
    'https://myproject.com',
    'https://www.myproject.com',
]
ALLOWED_HOSTS = [
    'myproject.com',
    'www.myproject.com',
]
```

### Optional Settings
| Setting | Description | Default |
|---------|-------------|---------|
| `CURRENCY_CODE` | Currency code for payments | `'USD'` |
| `CURRENCY_SYMBOL` | Currency symbol for display | `'$'` |
| `PROCESSORS` | Enabled payment processors | `['stripe']` |

See `SETUP.md` for detailed configuration instructions.

## Translation System

This project uses a custom database-driven translation system (not Django's built-in i18n).

**Setup:**
```bash
python manage.py set_languages  # Load languages from JSON
```

**Add translations:**
1. Go to Admin > Translations > Text bases
2. Add entries with `code_name` (identifier) and `text` (English)
3. Run `python manage.py run_translation` (requires Google Translate API key)

**Use in templates:**
```html
{{ g.i18n.your_code_name|default:"Fallback text" }}
{{ g.currency_symbol }}{{ price }}
{{ g.project_name }}
```

**Use in views:**
```python
from translations.models.translation import Translation
i18n = Translation.get_text_by_lang('en')
```

## Email Setup

This template uses native SMTP email (Postfix) instead of third-party services. See `EMAIL_SETUP.md` for:
- Postfix installation and configuration
- DKIM/SPF/DMARC DNS setup
- Testing email deliverability

For development, use console backend in `config.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

## Payment Processing

Supports multiple payment processors. Configure in `config.py`:

1. **Stripe** - Credit card payments
2. **PayPal** - PayPal checkout and subscriptions
3. **Square** - Square payments
4. **Coinbase** - Cryptocurrency payments

Setup PayPal subscriptions:
```bash
python manage.py create_paypal_product
python manage.py create_paypal_plans
```

## Template Variables

All templates have access to the `g` context:
- `{{ g.project_name }}` - Project name from config
- `{{ g.currency_symbol }}` - Currency symbol ($, €, etc.)
- `{{ g.currency_code }}` - Currency code (USD, EUR, etc.)
- `{{ g.i18n.key }}` - Translated text
- `{{ g.lang }}` - Current language
- `{{ g.languages }}` - All languages

## Creating a New Project

1. Clone this template
2. Run `python customize.py` for interactive setup
3. Or manually update `config.py` with your settings
4. Customize templates in `templates/`
5. Set up email DNS records
6. Configure payment processors

## Project Structure

```
├── app/              # Django settings and main URLs
├── accounts/         # Custom user model and auth
├── core/             # Main app (views, URLs)
├── contact_messages/ # Contact form handling
├── finances/         # Payment processing
├── translations/     # Database translation system
├── templates/        # HTML templates (Bootstrap 5)
├── static/           # CSS, JS, images
├── ansible/          # Server deployment playbooks
├── config_example.py # Template for config.py (copy to config.py)
├── customize.py      # Interactive setup script
├── SETUP.md          # Detailed setup guide
├── EMAIL_SETUP.md    # Email configuration guide
└── CLAUDE.md         # AI assistant instructions
```

## What's in .gitignore (and Why)

These files contain secrets or are environment-specific - **never commit them**:

| File/Pattern | Why It's Ignored | What To Do |
|--------------|------------------|------------|
| `config.py` | Contains SECRET_KEY, database passwords, API keys | Copy `config_example.py` → `config.py` and edit |
| `ansible/group_vars/all` | SSH credentials, server passwords | Copy `all.example` → `all` and edit |
| `ansible/servers` | Server IP addresses | Copy `servers.example` → `servers` and edit |
| `*/migrations/*.py` | Auto-generated, can differ between environments | Run `python manage.py migrate` on each server |
| `venv/` | Python virtual environment | Run `pip install -r requirements.txt` |
| `staticfiles/` | Collected static files for production | Run `python manage.py collectstatic` |
| `*.log`, `*.sql`, `*.csv` | Runtime/data files | Generated during operation |

**Important:** Each deployment (local, staging, production) needs its own `config.py` with appropriate settings.

## Server Deployment (Ubuntu 24.04)

**Step 1: Initial server setup (run ONCE on fresh server)**
```bash
cd ansible
cp servers.example servers          # Add your server IP
cp group_vars/all.example group_vars/all  # Add your credentials

# Add your SSH key to root
ssh-copy-id root@your-server-ip

# Create deploy user and DISABLE root login
ansible-playbook -i servers disableroot.yml -e "ansible_user=root"
```

**Step 2: Deploy application**
```bash
ansible-playbook -i servers djangodeployubuntu24.yml --tags=all,first_run
```

**Subsequent deployments:**
```bash
ansible-playbook -i servers gitpull.yml
```

> **Warning:** After `disableroot.yml` runs, root SSH is permanently disabled. All future access uses the deploy user defined in `group_vars/all`.

See `SETUP.md` for detailed deployment instructions.

## Requirements

- Python 3.10+
- Django 6.0+
- PostgreSQL
- Redis
- Postfix (for email)
