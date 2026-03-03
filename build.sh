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

if [[ "$CREATE_SUPERUSER" == "True" ]];
then
    python manage.py createsuperuser --noinput
fi

echo "=========================================="
echo "Build completed successfully!"
echo "=========================================="
