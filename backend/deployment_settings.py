"""
Django production settings for Render.com
"""

import os
import dj_database_url
from .settings import *  # noqa

# ==================================================
# SECURITY SETTINGS
# ==================================================

DEBUG = False

# Render hostname (DO NOT include https://)
RENDER_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "my-system-1-8al8.onrender.com")

# ALLOWED_HOSTS - include both environment variable and Render's hostname
_render_hostname = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "")
_allowed_hosts_env = os.environ.get("ALLOWED_HOSTS", "")
if _allowed_hosts_env:
    _hosts_list = _allowed_hosts_env.split(",")
else:
    _hosts_list = []
if _render_hostname and _render_hostname not in _hosts_list:
    _hosts_list.append(_render_hostname)
ALLOWED_HOSTS = _hosts_list




# CSRF trusted origins (must include https://)
CSRF_TRUSTED_ORIGINS = [
    f"https://{RENDER_HOSTNAME}",
]

# Secret Key (MUST be set in Render Environment Variables)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is required for production")

# ==================================================
# MIDDLEWARE
# ==================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==================================================
# DATABASE CONFIGURATION (Render PostgreSQL)
# ==================================================

DATABASE_URL = os.environ.get("DATABASE_URL")



# ==================================================
# STATIC FILES
# ==================================================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ==================================================
# CORS CONFIGURATION
# ==================================================

# CORS_ALLOWED_ORIGINS = [
#     "https://my-system-caaz.onrender.com",
# ]

CORS_ALLOW_CREDENTIALS = True



# ==================================================
# EMAIL CONFIGURATION
# ==================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    f"noreply@{RENDER_HOSTNAME}",
)

# ==================================================
# LOGGING
# ==================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

if [[SECRETE_SUPERUSER]]: 
    then
    python manage.py createsuperuser --not -input
fi

