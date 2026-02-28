"""
WSGI config for PC Maintenance Management System
"""

import os

from django.core.wsgi import get_wsgi_application

# Use deployment settings if RENDER_EXTERNAL_HOSTNAME is set (Render.com deployment)
setting_module = 'backend.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
