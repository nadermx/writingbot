# DjangoBase Setup Guide

This guide helps you create a new project from this Django 5.x base template.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/djangobase.git myproject
cd myproject

# 2. Run the customization script
python customize.py

# 3. Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up database
python manage.py migrate
python manage.py set_languages
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

## What the Customize Script Does

The `customize.py` script will prompt you for:
- **Project Name** (e.g., "MyApp") - Used in templates, emails, and admin
- **Project Domain** (e.g., "myapp.com") - Used for email sending and links
- **Database Name** (e.g., "myapp") - PostgreSQL database name

It automatically updates:
- `config.py` - All project settings
- `ansible/group_vars/all` - Deployment configuration
- Translation placeholders

## Configuration Reference

### config.py (Required Settings)

After running `customize.py`, review and update these values:

```python
# =============================================================================
# Project Settings
# =============================================================================
PROJECT_NAME = 'YourProject'
PROJECT_DOMAIN = 'yourproject.com'
ROOT_DOMAIN = 'https://yourproject.com'  # Production URL

# =============================================================================
# Security - CRITICAL for Production
# =============================================================================
# Generate a unique secret key:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'your-unique-secret-key-here'
DEBUG = False  # MUST be False in production

# Django 4+ requirement - prevents 403 CSRF errors
CSRF_TRUSTED_ORIGINS = [
    'https://yourproject.com',
    'https://www.yourproject.com',
]

ALLOWED_HOSTS = [
    'yourproject.com',
    'www.yourproject.com',
]

# =============================================================================
# Currency (Optional - defaults to USD/$)
# =============================================================================
CURRENCY_CODE = 'USD'
CURRENCY_SYMBOL = '$'

# =============================================================================
# Database
# =============================================================================
DATABASE = {
    'default': {
        'NAME': 'yourproject',
        'USER': 'postgres',
        'PASSWORD': 'your-secure-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# =============================================================================
# Payment Processors
# =============================================================================
PROCESSORS = ['stripe']  # Options: 'stripe', 'squareup', 'paypal', 'coinbase'

STRIPE = {
    'pk': 'pk_live_xxx',
    'sk': 'sk_live_xxx',
}

# Google Translate API (optional, for auto-translations)
GOOGLE_API = 'your-api-key'
```

## Self-Hosted Email Setup (Required for Production)

This template uses **self-hosted email via Postfix** (no third-party email services required).

### Development Mode
For development, use console backend to see emails in terminal:
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production Mode
1. **Run the Ansible playbook** to install Postfix + OpenDKIM:
   ```bash
   cd ansible
   # Edit setup_email.yml with your domain and forward email
   ansible-playbook -i servers setup_email.yml
   ```

2. **Add DNS records** (the playbook will output these):
   - A record: `mail.yourdomain.com` → your server IP
   - MX record: `@ → mail.yourdomain.com`
   - SPF record: `v=spf1 ip4:YOUR_IP a mx ~all`
   - DMARC record: `v=DMARC1; p=quarantine; rua=mailto:you@email.com`
   - DKIM record: (from playbook output)

3. **Update config.py**:
   ```python
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'localhost'
   EMAIL_PORT = 25
   EMAIL_USE_TLS = False
   EMAIL_HOST_USER = ''
   EMAIL_HOST_PASSWORD = ''
   DEFAULT_FROM_EMAIL = f'{PROJECT_NAME} <noreply@mail.{PROJECT_DOMAIN}>'
   SERVER_EMAIL = f'server@mail.{PROJECT_DOMAIN}'
   ```

**See `EMAIL_SETUP.md` for complete instructions, troubleshooting, and testing.**

## Ansible Deployment Setup (Ubuntu 24.04)

### Initial Setup

1. **Copy example files:**
   ```bash
   cp ansible/group_vars/all.example ansible/group_vars/all
   cp ansible/servers.example ansible/servers
   ```

2. **Update `ansible/servers`** with your server IP

3. **Update `ansible/group_vars/all`** with:
   - `deploy_user` - Username for deploy account (e.g., `myproject`)
   - `deploy_password` - Secure password for deploy user
   - `db_name`, `db_user`, `db_password` - PostgreSQL credentials
   - `githuburl` - Your repository URL
   - `projectname` - Used for nginx/supervisor configs
   - `domain` - Your domain name

### First Deployment (New Server)

```bash
cd ansible

# Step 1: Add your SSH key to root
ssh-copy-id root@your-server-ip

# Step 2: Create deploy user and disable root (run once)
ansible-playbook -i servers disableroot.yml -e "ansible_user=root"

# Step 3: Deploy the application
ansible-playbook -i servers djangodeployubuntu24.yml --tags=all,first_run
```

After `disableroot.yml` runs, root login is **permanently disabled**. All future connections use the deploy user.

### Subsequent Deployments

```bash
# Quick code update
ansible-playbook -i servers gitpull.yml

# Full redeploy (reinstalls packages, updates configs)
ansible-playbook -i servers djangodeployubuntu24.yml
```

### Post-Deployment

```bash
# Set up SSL
ansible -i servers all -m shell -a "certbot --nginx -d yourdomain.com" --become

# Create config.py on server
ansible -i servers all -m shell -a "cp /home/www/myproject/config_example.py /home/www/myproject/config.py" --become-user=myproject --become

# Run migrations
ansible -i servers all -m shell -a "/home/www/myproject/venv/bin/python /home/www/myproject/manage.py migrate" --become-user=myproject --become
```

## Adding Translations

1. Go to Django admin → Translations → Text bases
2. Add new entries with unique `code_name` (e.g., `welcome_message`)
3. Run auto-translation:
   ```bash
   python manage.py run_translation
   ```
4. Use in templates:
   ```html
   {{ g.i18n.welcome_message|default:"Welcome" }}
   ```

## Setting Up Plans

Edit `finances/json/plans.json` or use Django admin:

```json
{
    "starter": {
        "code_name": "starter",
        "price": 9,
        "credits": 100,
        "days": 31,
        "subscription": true
    }
}
```

Then run:
```bash
python manage.py set_plans
```

## Payment Processor Setup

### Stripe
1. Get API keys from https://dashboard.stripe.com/apikeys
2. Add to `config.py`:
   ```python
   STRIPE = {
       'pk': 'pk_live_xxx',
       'sk': 'sk_live_xxx',
   }
   ```

### PayPal (for subscriptions)
1. Get credentials from https://developer.paypal.com
2. Add to `config.py`:
   ```python
   PAYPAL_KEYS = {
       'id': 'your-client-id',
       'secret': 'your-secret',
       'api': 'https://api-m.paypal.com',  # Use sandbox URL for testing
       'env': 'live',
   }
   ```
3. Run setup commands:
   ```bash
   python manage.py create_paypal_product
   python manage.py create_paypal_plans
   ```

### Square
1. Get credentials from https://developer.squareup.com
2. Add to `config.py`:
   ```python
   SQUARE_UP = {
       'env': 'production',  # or 'sandbox'
       'id': 'your-app-id',
       'secret': 'your-secret',
   }
   ```

## Template Variables

All templates have access to the `g` context:

| Variable | Description |
|----------|-------------|
| `{{ g.project_name }}` | Project name from config |
| `{{ g.currency_symbol }}` | Currency symbol ($, €, etc.) |
| `{{ g.currency_code }}` | Currency code (USD, EUR, etc.) |
| `{{ g.i18n.key }}` | Translated text |
| `{{ g.lang }}` | Current language object |
| `{{ g.languages }}` | All available languages |
| `{{ g.scripts_version }}` | For cache busting |

## Customizing Templates

Key templates to customize:

| Template | Purpose |
|----------|---------|
| `templates/index.html` | Homepage |
| `templates/about.html` | About page (add your story) |
| `templates/pricing.html` | Pricing page |
| `templates/terms.html` | Terms of Service |
| `templates/privacy.html` | Privacy Policy |
| `static/css/styles.css` | Custom styles |

## Production Deployment

1. **Update `config.py`:**
   ```python
   DEBUG = False
   ROOT_DOMAIN = 'https://yourdomain.com'
   SECRET_KEY = 'your-unique-production-key'
   CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']
   ALLOWED_HOSTS = ['yourdomain.com']
   ```

2. **Set up email** (see EMAIL_SETUP.md)

3. **Deploy with Ansible:**
   ```bash
   cd ansible
   ansible-playbook -i servers djangodeployubuntu20.yml
   ```

4. **Set up SSL:**
   ```bash
   ansible -i servers all -m shell -a "certbot --nginx -d yourdomain.com" --become
   ```

5. **Set up cron jobs:**
   ```bash
   # Daily subscription billing
   0 0 * * * /home/www/myproject/venv/bin/python /home/www/myproject/manage.py rebill

   # Expire inactive subscriptions
   0 1 * * * /home/www/myproject/venv/bin/python /home/www/myproject/manage.py expire_pro_users
   ```

## File Structure Overview

```
├── accounts/         # User authentication, credits, subscriptions
├── app/              # Django settings, utilities
├── core/             # Main views (pages, checkout, auth)
├── finances/         # Payment processing
├── translations/     # Database translation system
├── templates/        # HTML templates
├── static/           # CSS, JS, images
├── ansible/          # Server deployment
├── config.py         # Your settings (gitignored)
├── config_example.py # Template for config.py
├── SETUP.md          # This file
├── EMAIL_SETUP.md    # Complete email setup guide
└── CLAUDE.md         # AI assistant instructions
```

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

# Deployment
cd ansible && ansible-playbook -i servers gitpull.yml
```

## Files You Must Create (Not in Git)

These files are in `.gitignore` because they contain secrets or environment-specific settings:

| File | Template | Purpose |
|------|----------|---------|
| `config.py` | `config_example.py` | All project settings, API keys, database passwords |
| `ansible/group_vars/all` | `ansible/group_vars/all.example` | SSH credentials, server passwords |
| `ansible/servers` | `ansible/servers.example` | Server IP addresses |

**Each environment (local, staging, production) needs its own copies of these files.**

```bash
# First time setup
cp config_example.py config.py
cp ansible/group_vars/all.example ansible/group_vars/all
cp ansible/servers.example ansible/servers
# Then edit each file with your values
```

## Logging

This project uses StreamHandler to output logs to stderr, which supervisor captures automatically. This approach is simpler than managing separate log files and ensures all output is in one place.

### Backend Errors
Django errors are logged to stderr and captured by supervisor:
```bash
# View recent errors
ansible -i servers all -m shell -a "tail -100 /var/log/{project}/{project}.err.log" --become

# Follow logs in real-time
ansible -i servers all -m shell -a "tail -f /var/log/{project}/{project}.err.log" --become
```

### Frontend Errors
JavaScript errors are automatically captured and logged via the `/api/accounts/log-error/` endpoint. The error handler in `base.html` catches:
- `window.onerror` - Uncaught JavaScript errors
- `unhandledrejection` - Unhandled Promise rejections

Frontend errors appear in the same supervisor log with prefix `FRONTEND ERROR:`.

### Custom Logging
To add logging in your code:
```python
import logging
logger = logging.getLogger('app')

# In your code
logger.warning('User %s attempted invalid action', user.id)
logger.error('Payment failed', exc_info=True)  # includes stack trace
```

### Log Configuration
The logging config in `config.py` defines two loggers:
- `django` - Django framework errors (level: ERROR)
- `app` - Application logs including frontend errors (level: WARNING)

## Troubleshooting

### CSRF 403 Errors (Django 4+)

This is the most common issue. Django 4+ requires `CSRF_TRUSTED_ORIGINS` to include your domain with the protocol.

**Fix:** Add your domains to `config.py`:
```python
# MUST include the protocol (https:// or http://)
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
    # For local development:
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# Also update ALLOWED_HOSTS:
ALLOWED_HOSTS = [
    'yourdomain.com',
    'www.yourdomain.com',
    'localhost',
    '127.0.0.1',
]
```

**Note:** If you're getting 403 errors on forms, this is almost always the cause.

### Database connection error
- Check PostgreSQL is running: `sudo systemctl status postgresql`
- Verify credentials in `config.py`

### Email not sending
- Check Postfix status: `sudo systemctl status postfix`
- Test with console backend first
- Verify DNS records (SPF, DKIM, DMARC)
- See `EMAIL_SETUP.md` for detailed troubleshooting

### Static files not loading
- Run `python manage.py collectstatic`
- Check nginx config serves `/static/` correctly

### Payment webhook errors
- Verify webhook URLs are accessible
- Check processor-specific logs in Django admin
