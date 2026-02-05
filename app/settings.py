"""
Django settings for WritingBot.ai project.
"""

from pathlib import Path
import os
import config
from config import *

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security
SECRET_KEY = config.SECRET_KEY
DEBUG = config.DEBUG
ALLOWED_HOSTS = getattr(config, 'ALLOWED_HOSTS', ['*'])
CSRF_TRUSTED_ORIGINS = getattr(config, 'CSRF_TRUSTED_ORIGINS', [])

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'rest_framework',
    'django_rq',
    'django_select2',
    'captcha',
    # Core apps (from djangobase)
    'translations',
    'accounts',
    'contact_messages',
    'finances',
    'core',
    # WritingBot tool apps
    'paraphraser',
    'grammar',
    'summarizer',
    'ai_detector',
    'humanizer',
    'plagiarism',
    'translator',
    'citations',
    'flow',
    'ai_tools',
    'word_counter',
    'pdf_tools',
    'media_tools',
    'courses',
    'blog',
    'seo',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'app.wsgi.application'

# Database
DATABASES = DATABASE
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    },
    'select2': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

SELECT2_CACHE_BACKEND = 'select2'

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

# Redis Queue
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    },
    'low': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'DEFAULT_TIMEOUT': 360,
    }
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/hour',
        'user': '1000/hour'
    }
}

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# AI Service Configuration
ANTHROPIC_API_KEY = getattr(config, 'ANTHROPIC_API_KEY', '')
ANTHROPIC_MODEL = getattr(config, 'ANTHROPIC_MODEL', 'claude-sonnet-4-5-20250929')
TRANSLATEAPI_KEY = getattr(config, 'TRANSLATEAPI_KEY', '')

# Tool Limits (free tier)
TOOL_LIMITS = {
    'paraphraser': {'free_words': 500, 'free_modes': ['standard', 'fluency']},
    'grammar': {'free_words': 5000},
    'summarizer': {'free_words': 1200, 'premium_words': 6000},
    'ai_detector': {'free_words': 1200},
    'humanizer': {'free_words': 500},
    'translator': {'free_chars': 5000},
    'ai_tools': {'free_daily': 50},
    'pdf_tools': {'free_daily': 3},
    'plagiarism': {'premium_monthly_words': 30000},
}

# Logging
LOGGING = config.LOGGING
