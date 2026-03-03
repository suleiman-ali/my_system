#!/bin/bash
# Build script for deployment on Render.com or similar platforms
# This script runs during the build phase on Render

set -o errexit

echo "=========================================="
echo "Starting Django Backend Build for Render"
echo "=========================================="

# Install Python dependencies
echo "[1/4] Installing Python dependencies..."
pip install -r requirements.txt

# Run migrations (NO makemigrations in production - migrations should be committed)
echo "[2/4] Running database migrations..."
python manage.py migrate --noinput

# Collect static files for WhiteNoise
echo "[3/4] Collecting static files..."
python manage.py collectstatic --noinput

if [[ "${CREATE_SUPERUSER,,}" == "true" ]]; then
    echo "[4/4] Creating/updating deployment superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
import os

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not username or not email or not password:
    raise SystemExit('Missing DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL, or DJANGO_SUPERUSER_PASSWORD')

user, created = User.objects.get_or_create(username=username, defaults={'email': email})
user.email = email
user.is_staff = True
user.is_superuser = True
if hasattr(user, 'is_admin'):
    user.is_admin = True
user.set_password(password)
user.save()

print('Superuser created' if created else 'Superuser updated')
"
fi

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
