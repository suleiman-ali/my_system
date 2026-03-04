from django.db import migrations

def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.create_superuser(
        username='admin',
        email='admin@gmail.com',
        password='admin@1234',
    )

class Migration(migrations.Migration):
    dependencies = [
        ('yourappname', 'last_migration_file'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]
