#!/usr/bin/env python
"""
Script to create a Django superuser if it doesn't exist.
Usage: python create_superuser.py
"""
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KishorelinBlog.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Get credentials from environment variables (or use defaults)
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'aruldha')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'aruldha@uwindsor.ca')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Arulmabel@95')

# Create superuser if it doesn't exist
if not User.objects.filter(username=ADMIN_USERNAME).exists():
    User.objects.create_superuser(
        username=ADMIN_USERNAME,
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD
    )
    print(f"✅ Superuser '{ADMIN_USERNAME}' created successfully!")
    print(f"   Email: {ADMIN_EMAIL}")
    print(f"   Password: {ADMIN_PASSWORD}")
    print("\n⚠️  IMPORTANT: Change the password after first login!")
else:
    print(f"ℹ️  Superuser '{ADMIN_USERNAME}' already exists. Skipping creation.")

