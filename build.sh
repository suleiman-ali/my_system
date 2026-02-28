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

# Create superuser if requested (optional)
if [[ "$CREATE_SUPERUSER" == "True" ]]; then
  echo "[4/4] Creating superuser..."
  # Set password via environment variable to avoid interactive prompt
  export DJANGO_SUPERUSER_PASSWORD="${DJANGO_SUPERUSER_PASSWORD:-}"
  echo "from django.contrib.auth import get_user_model; User = get_user_model(); 
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser(
        username='$DJANGO_SUPERUSER_USERNAME',
        email='$DJANGO_SUPERUSER_EMAIL',
        password='$DJANGO_SUPERUSER_PASSWORD'
    )" | python manage.py shell
fi

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
