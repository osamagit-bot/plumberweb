#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'plumber_site.settings')
django.setup()

from django.core.mail import send_mail
from django.contrib.auth.models import User

# Test email sending
print("Testing email backend...")

# Check if user exists
try:
    user = User.objects.get(email='khanhemasa@gmail.com')
    print(f"User found: {user.username} ({user.email})")
except User.DoesNotExist:
    print("User with email 'khanhemasa@gmail.com' does not exist!")
    print("Creating test user...")
    user = User.objects.create_user(
        username='testuser',
        email='khanhemasa@gmail.com',
        password='testpass123'
    )
    print(f"Created user: {user.username} ({user.email})")

# Test sending email
try:
    send_mail(
        'Test Email',
        'This is a test email to verify the console backend is working.',
        'noreply@sproplumbing.com',
        ['khanhemasa@gmail.com'],
        fail_silently=False,
    )
    print("Email sent successfully! Check console output above.")
except Exception as e:
    print(f"Error sending email: {e}")