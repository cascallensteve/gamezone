#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamezone.settings')
django.setup()

from rentals.models import CustomUser

print("=== SETTING UP ADMIN USER FOR CUSTOM ADMIN PANEL ===")
print()

# Check if admin user exists
admin_user = CustomUser.objects.filter(email='admin@gamezone.com').first()

if admin_user:
    print(f"✅ Admin user found:")
    print(f"   Email: {admin_user.email}")
    print(f"   Username: {admin_user.username}")
    print(f"   Is Staff: {admin_user.is_staff}")
    print(f"   Is Superuser: {admin_user.is_superuser}")
    print(f"   Role: {admin_user.role}")
    print()
    
    # Ensure admin privileges
    needs_update = False
    
    if not admin_user.is_staff:
        admin_user.is_staff = True
        needs_update = True
        print("   🔧 Making user staff member...")
    
    if not admin_user.is_superuser:
        admin_user.is_superuser = True
        needs_update = True
        print("   🔧 Making user superuser...")
    
    if admin_user.role != 'admin':
        admin_user.role = 'admin'
        needs_update = True
        print("   🔧 Setting role to admin...")
    
    if needs_update:
        admin_user.save()
        print("   ✅ Admin privileges updated!")
    
    print()
    print("🎯 ADMIN LOGIN CREDENTIALS:")
    print("   Email: admin@gamezone.com")
    print("   Password: [You need to know this]")
    print()
    print("�� CUSTOM ADMIN PANEL URL:")
    print("   http://127.0.0.1:8000/admin-login/")
    
else:
    print("❌ No admin user found. Creating one...")
    print()
    
    # Create admin user
    admin_user = CustomUser.objects.create_user(
        username='admin',
        email='admin@gamezone.com',
        password='admin123',  # You can change this after first login
        first_name='Admin',
        last_name='User',
        role='admin',
        is_staff=True,
        is_superuser=True,
        is_email_verified=True
    )
    
    print("✅ Admin user created successfully!")
    print()
    print("🎯 ADMIN LOGIN CREDENTIALS:")
    print("   Email: admin@gamezone.com")
    print("   Password: admin123")
    print("   ⚠️  Please change password after first login!")
    print()
    print("�� CUSTOM ADMIN PANEL URL:")
    print("   http://127.0.0.1:8000/admin-login/")

print()
print("=== NEXT STEPS ===")
print("1. Run this script: python setup_admin.py")
print("2. Visit: http://127.0.0.1:8000/admin-login/")
print("3. Log in with the credentials above")
print("4. You'll be redirected to your custom admin panel") 