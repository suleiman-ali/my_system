"""
Django deployment settings for production (Render.com or similar)
Import from base settings and override for production environment
"""

import os
import dj_database_url
from .settings import *  # noqa: F401, F403

# ===== SECURITY SETTINGS =====
DEBUG = False

# Set ALLOWED_HOSTS from environment variable (required for production)
# Get Render's provided hostname or use environment variable
RENDER_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME', os.environ.get('ALLOWED_HOSTS', ''))
ALLOWED_HOSTS = [
    RENDER_HOSTNAME,
    'localhost',
    '127.0.0.1',
]

# CSRF and Security settings
render_origin = f"https://{RENDER_HOSTNAME}" if RENDER_HOSTNAME else None
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []
if render_origin and render_origin not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append(render_origin)

# Secret key must be set in environment variable
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('SECRET_KEY environment variable is required for production')

# ===== MIDDLEWARE =====
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===== DATABASE CONFIGURATION =====
# Parse DATABASE_URL from Render (PostgreSQL)
# Fallback to SQLite if DATABASE_URL is not set (for initial setup)
db_url = os.environ.get('DATABASE_URL')
if db_url:
    DATABASES = {
        'default': dj_database_url.config(
            default=db_url,
            conn_max_age=600,
            ssl_require=True,  # Required for Render PostgreSQL
        )
    }
else:
    # Fallback to SQLite for initial deployment testing
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ===== STATIC FILES & STORAGE =====
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    }
}

# ===== CORS CONFIGURATION =====
# Configure CORS properly for production
# Get from environment or use frontend URL from Render
cors_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
if cors_origins:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in cors_origins.split(',') if origin.strip()]
else:
    # Default: allow the Render frontend if configured
    frontend_url = os.environ.get('FRONTEND_URL', '')
    if frontend_url:
        CORS_ALLOWED_ORIGINS = [frontend_url]
    else:
        # Fallback placeholder - UPDATE THIS with your actual frontend URL
        CORS_ALLOWED_ORIGINS = [
            'https://your-frontend.onrender.com',  # TODO: Replace with your actual frontend URL
        ]

CORS_ALLOW_CREDENTIALS = True

# ===== SECURITY HEADERS =====
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ===== EMAIL CONFIGURATION (Optional) =====
# Configure these in environment variables
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'noreply@example.com')

# ===== LOGGING FOR PRODUCTION =====
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
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
