#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamezone.settings')
django.setup()

from rentals.models import CustomUser

print("=== EXISTING ADMIN USERS ===")
print()

# Get all users
users = CustomUser.objects.all()

if not users.exists():
    print("No users found in database.")
else:
    print(f"Found {users.count()} user(s) in database:")
    print()
    
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Is Staff: {user.is_staff}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Active: {user.is_active}")
        print("-" * 50)

print()
print("=== ADMIN LOGIN DETAILS ===")
print()

# Find admin users
admin_users = CustomUser.objects.filter(is_staff=True)

if admin_users.exists():
    print("Admin users that can access the admin panel:")
    print()
    for user in admin_users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Password: [You need to know this]")
        print(f"Role: {user.role}")
        print("-" * 30)
else:
    print("No admin users found. You need to create one.")

print()
print("=== LOGIN URLs ===")
print("Custom Admin Panel: http://localhost:8000/admin-panel/")
print("Django Admin: http://localhost:8000/admin/")
print("Login Page: http://localhost:8000/accounts/login/") 