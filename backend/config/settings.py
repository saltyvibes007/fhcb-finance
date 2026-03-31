import os
from pathlib import Path
from datetime import timedelta
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-insecure-key")

# ---------------------------------------------------------------------------
# Branch-aware environment config (follows RTT pattern)
# Railway auto-provides RAILWAY_GIT_BRANCH and RAILWAY_GIT_COMMIT_SHA.
# ---------------------------------------------------------------------------
GIT_BRANCH = os.environ.get("RAILWAY_GIT_BRANCH", os.environ.get("GIT_BRANCH", "main"))
GIT_COMMIT = os.environ.get("RAILWAY_GIT_COMMIT_SHA", os.environ.get("GIT_COMMIT", "unknown"))

IS_PRODUCTION = GIT_BRANCH == "main"

import sys
_argv0 = sys.argv[0] if sys.argv else ''
if 'runserver' in _argv0 or 'gunicorn' in _argv0:
    print(f"[DJANGO] Branch: {GIT_BRANCH}, Production: {IS_PRODUCTION}, Commit: {GIT_COMMIT}")

BASE_DOMAIN = "corp.bloomfi.ai"

# Calculated URLs — branch-prefixed subdomain for non-prod
# Production: backend-corp.bloomfi.ai / corp.bloomfi.ai
# UAT:        uat-backend-corp.bloomfi.ai / uat-corp.bloomfi.ai
if IS_PRODUCTION:
    BACKEND_URL = f"https://backend-{BASE_DOMAIN}"
    FRONTEND_URL = f"https://{BASE_DOMAIN}"
else:
    BACKEND_URL = f"https://{GIT_BRANCH}-backend-{BASE_DOMAIN}"
    FRONTEND_URL = f"https://{GIT_BRANCH}-{BASE_DOMAIN}"

DEBUG = not IS_PRODUCTION if os.environ.get("DEBUG") is None else os.environ.get("DEBUG", "false").lower() == "true"

ALLOWED_HOSTS = [
    f"{GIT_BRANCH}-backend-{BASE_DOMAIN}" if not IS_PRODUCTION else f"backend-{BASE_DOMAIN}",
    f"backend-{BASE_DOMAIN}",
    f"uat-backend-{BASE_DOMAIN}",
    "localhost",
    "127.0.0.1",
    ".up.railway.app",
    "healthcheck.railway.app",
] + [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h]

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
]

LOCAL_APPS = [
    'accounts',
    'transactions',
    'reports',
    'chat',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.parse(os.getenv('DATABASE_URL'), conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS — derived from branch (follows RTT pattern)
CORS_ALLOW_ALL_ORIGINS = DEBUG
_branch_cors_origins = [
    FRONTEND_URL,
    f"https://www.{BASE_DOMAIN}",
]
_env_cors = [o for o in os.environ.get("CORS_ALLOWED_ORIGINS", "").split(",") if o]
CORS_ALLOWED_ORIGINS = list(set(_branch_cors_origins + _env_cors)) if not DEBUG else []
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept", "authorization", "content-type", "origin",
    "x-csrftoken", "x-requested-with",
]

# CSRF
CSRF_TRUSTED_ORIGINS = [FRONTEND_URL, BACKEND_URL]

# OpenAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Admin Password
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin123')

# File Upload
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
