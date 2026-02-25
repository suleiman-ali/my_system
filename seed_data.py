"""
Seed data script for PC Maintenance Management System
Creates admin user and initial services
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
from services.models import Service

User = get_user_model()

def create_admin():
    """Create admin user if not exists"""
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@pcfix.com',
            password='admin123',
            is_admin=True
        )
        print(f"Admin user created: {admin.username}")
    else:
        print("Admin user already exists")

def create_services():
    """Create initial services if not exists"""
    services_data = [
        {
            'name': 'Virus & Malware Removal',
            'description': 'Complete virus and malware removal from your computer. Includes full system scan, malware removal, and security software installation.',
            'price': 50000.00
        },
        {
            'name': 'Hardware Repair/Replacement',
            'description': 'Diagnosis and repair or replacement of faulty hardware components including RAM, hard drive, keyboard, screen, and other parts.',
            'price': 100000.00
        },
        {
            'name': 'Software Installation',
            'description': 'Installation of software applications including Microsoft Office, Adobe, browsers, and other commonly used software.',
            'price': 30000.00
        },
        {
            'name': 'System Format & Reinstall',
            'description': 'Complete system format and Windows reinstallation with all necessary drivers and updates.',
            'price': 80000.00
        },
        {
            'name': 'Data Recovery',
            'description': 'Recovery of lost or deleted data from hard drives, USB drives, memory cards, and other storage devices.',
            'price': 150000.00
        },
        {
            'name': 'RAM Upgrade',
            'description': 'Installation of additional RAM or replacement with higher capacity memory modules.',
            'price': 100000.00
        },
        {
            'name': 'Hard Drive Replacement',
            'description': 'Replacement of faulty hard drive with new SSD or HDD, including data transfer if possible.',
            'price': 80000.00
        },
        {
            'name': 'Screen Repair/Replacement',
            'description': 'Repair or replacement of cracked or damaged laptop/PC screens.',
            'price': 50000.00
        },
        {
            'name': 'Keyboard Repair',
            'description': 'Repair or replacement of faulty keyboard keys or entire keyboard.',
            'price': 30000.00
        },
        {
            'name': 'General Cleaning & Maintenance',
            'description': 'Complete internal cleaning, thermal paste replacement, fan cleaning, and overall system maintenance.',
            'price': 40000.00
        },
    ]
    
    for service_data in services_data:
        if not Service.objects.filter(name=service_data['name']).exists():
            Service.objects.create(**service_data)
            print(f"Created service: {service_data['name']}")
        else:
            print(f"Service already exists: {service_data['name']}")

if __name__ == '__main__':
    print("Seeding data...")
    create_admin()
    create_services()
    print("Data seeding completed!")
