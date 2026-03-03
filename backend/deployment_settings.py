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
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://my-sistems.vercel.app").rstrip("/")

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
_csrf_trusted_env = os.environ.get("CSRF_TRUSTED_ORIGINS", "")
if _csrf_trusted_env:
    CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in _csrf_trusted_env.split(",") if origin.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        f"https://{RENDER_HOSTNAME}",
        FRONTEND_URL,
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
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required in deployment")



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
WHITENOISE_MANIFEST_STRICT = False

# ==================================================
# CORS CONFIGURATION
# ==================================================

# Get CORS origins from environment variable or use default Render hostname
_cors_origins_env = os.environ.get("CORS_ALLOWED_ORIGINS", "")
if _cors_origins_env:
    CORS_ALLOWED_ORIGINS = [origin.strip() for origin in _cors_origins_env.split(",") if origin.strip()]
else:
    # Default to configured frontend URL
    CORS_ALLOWED_ORIGINS = [
        FRONTEND_URL,
    ]

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
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True,
    )
}

