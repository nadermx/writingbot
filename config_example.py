# =============================================================================
# Project Settings
# =============================================================================
# Copy this file to config.py and customize for your project

PROJECT_NAME = 'MyProject'
PROJECT_DOMAIN = 'example.com'  # Your domain (e.g., myproject.com)
ROOT_DOMAIN = 'http://localhost:8000'  # Full URL with protocol

# Security - REQUIRED: Generate a unique secret key for production
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'django-insecure-change-me-in-production'

# Debug mode - MUST be False in production
DEBUG = True

# =============================================================================
# CSRF Trusted Origins (Django 4+ requirement)
# =============================================================================
# Add your domain(s) here to fix 403 CSRF errors
# Include both http and https versions for development
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    # 'https://example.com',
    # 'https://www.example.com',
]

# Allowed hosts - Add your domain(s) here
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # 'example.com',
    # 'www.example.com',
]

# =============================================================================
# Currency Settings
# =============================================================================
CURRENCY_CODE = 'USD'
CURRENCY_SYMBOL = '$'

# =============================================================================
# Google Translate API (for translations)
# =============================================================================
GOOGLE_API = ''

# =============================================================================
# Email Configuration
# =============================================================================
# For production, set up Postfix on your server with DKIM/SPF/DMARC
# See EMAIL_SETUP.md for DNS setup

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'  # Use localhost for local Postfix
EMAIL_PORT = 25  # Standard SMTP port (or 587 for TLS relay)
EMAIL_USE_TLS = False  # Set True if using external relay
EMAIL_HOST_USER = ''  # Leave empty for local Postfix
EMAIL_HOST_PASSWORD = ''  # Leave empty for local Postfix
DEFAULT_FROM_EMAIL = f'{PROJECT_NAME} <no-reply@{PROJECT_DOMAIN}>'
SERVER_EMAIL = f'server@{PROJECT_DOMAIN}'

# For development, use console backend to see emails in terminal:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =============================================================================
# Database
# =============================================================================
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# =============================================================================
# Payment Processors
# =============================================================================
# Enable the processors you need
PROCESSORS = [
    'stripe',
    # 'squareup',
    # 'paypal',
    # 'coinbase',
]

# Stripe - https://dashboard.stripe.com/apikeys
STRIPE = {
    'pk': 'pk_test_xxx',
    'sk': 'sk_test_xxx',
}

# Square - https://developer.squareup.com/apps
SQUARE_UP = {
    'env': 'sandbox',  # 'sandbox' or 'production'
    'id': 'sandbox-xxx',
    'secret': 'xxx',
}

# PayPal - https://developer.paypal.com/dashboard/applications
PAYPAL_KEYS = {
    'id': 'your-paypal-client-id',
    'secret': 'your-paypal-secret',
    'api': 'https://api-m.sandbox.paypal.com',  # Use api-m.paypal.com for production
    'env': 'sandbox',  # 'sandbox' or 'live'
}

# =============================================================================
# Rate Limiting & Quotas
# =============================================================================
RATE_LIMIT = 10  # Requests per hour for unauthenticated users
FILES_LIMIT = 2147483648  # 2GB max file size

# =============================================================================
# Cache Busting
# =============================================================================
SCRIPT_VERSION = '1.0.0'  # Increment when static files change

# =============================================================================
# Logging
# =============================================================================
# Uses StreamHandler to output to stderr, which supervisor captures automatically.
# Logs appear in supervisor's stderr log file (e.g., /var/log/{project}/{project}.err.log)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'app': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}
