set -o errexit

# Change to root directory where requirements.txt is located
cd "$(dirname "$0")/.."

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate --noinput

if [[ "${CREATE_SUPERUSER,,}" == "true" ]]; then
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
