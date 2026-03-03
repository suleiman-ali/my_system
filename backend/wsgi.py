"""
WSGI config for PC Maintenance Management System
"""

import os

from django.core.wsgi import get_wsgi_application

# Use deployment settings on Render even if only the generic RENDER env is available.
is_render = 'RENDER' in os.environ or 'RENDER_EXTERNAL_HOSTNAME' in os.environ
setting_module = 'backend.deployment_settings' if is_render else 'backend.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
