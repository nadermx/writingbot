# =============================================================================
# WritingBot.ai - Configuration
# =============================================================================
# Copy this file to config.py and customize for your project

PROJECT_NAME = 'WritingBot.ai'
PROJECT_DOMAIN = 'writingbot.ai'
ROOT_DOMAIN = 'http://localhost:8000'  # Full URL with protocol

# Security - REQUIRED: Generate a unique secret key for production
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = 'django-insecure-change-me-in-production'

# Debug mode - MUST be False in production
DEBUG = True

# =============================================================================
# CSRF Trusted Origins (Django 4+ requirement)
# =============================================================================
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    # 'https://writingbot.ai',
    # 'https://www.writingbot.ai',
]

# Allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # 'writingbot.ai',
    # 'www.writingbot.ai',
]

# =============================================================================
# Currency Settings
# =============================================================================
CURRENCY_CODE = 'USD'
CURRENCY_SYMBOL = '$'

# =============================================================================
# AI Service Configuration
# =============================================================================
# Anthropic Claude API - Primary AI provider
ANTHROPIC_API_KEY = ''  # Get from https://console.anthropic.com/
ANTHROPIC_MODEL = 'claude-sonnet-4-5-20250929'  # Default model for tool operations

# Open-Source LLM API (served from GPU server via ollama)
WRITINGBOT_API_URL = 'https://api.writingbot.ai'
WRITINGBOT_API_KEY = ''  # Shared secret with GPU server

# Premium LLM: set to True to use Claude for premium users
USE_CLAUDE_FOR_PREMIUM = True

# Internal API secret (shared with GPU server for API key validation)
INTERNAL_API_SECRET = ''  # python -c "import secrets; print(secrets.token_urlsafe(32))"

# Translation API
TRANSLATEAPI_KEY = ''  # Get from https://translateapi.ai/

# =============================================================================
# Google Translate API (for i18n translations)
# =============================================================================
GOOGLE_API = ''

# =============================================================================
# Email Configuration
# =============================================================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = f'{PROJECT_NAME} <no-reply@mail.{PROJECT_DOMAIN}>'
SERVER_EMAIL = f'server@mail.{PROJECT_DOMAIN}'

# For development:
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# =============================================================================
# Database
# =============================================================================
DATABASE = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'writingbot',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# =============================================================================
# Payment Processors
# =============================================================================
PROCESSORS = [
    'stripe',
    # 'squareup',
    # 'paypal',
]

# Stripe - https://dashboard.stripe.com/apikeys
STRIPE = {
    'pk': 'pk_test_xxx',
    'sk': 'sk_test_xxx',
}

# Square - https://developer.squareup.com/apps
SQUARE_UP = {
    'env': 'sandbox',
    'id': 'sandbox-xxx',
    'secret': 'xxx',
}

# PayPal - https://developer.paypal.com/dashboard/applications
PAYPAL_KEYS = {
    'id': 'your-paypal-client-id',
    'secret': 'your-paypal-secret',
    'api': 'https://api-m.sandbox.paypal.com',
    'env': 'sandbox',
}

# =============================================================================
# Rate Limiting & Quotas
# =============================================================================
RATE_LIMIT = 10  # Requests per hour for unauthenticated users
FILES_LIMIT = 5242880  # 5MB max file size

# =============================================================================
# Cache Busting
# =============================================================================
SCRIPT_VERSION = '1.0.2'

# =============================================================================
# Logging
# =============================================================================
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
