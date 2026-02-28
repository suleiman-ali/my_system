"""
WSGI config for PC Maintenance Management System
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

setting_module= 'zenjitaste.deployment_settings' if 'RENDER_EXTERNAL_HOSTNAME' in os.environ else 'zenjitaste.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
