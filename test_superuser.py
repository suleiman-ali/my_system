import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Check if superuser exists
superusers = User.objects.filter(is_superuser=True)

with open('superuser_check.txt', 'w') as f:
    f.write(f"Number of superusers: {superusers.count()}\n")
    
    for u in superusers:
        f.write(f"Username: {u.username}, Email: {u.email}\n")
    
    # Also check total users
    all_users = User.objects.all()
    f.write(f"Total users: {all_users.count()}\n")
