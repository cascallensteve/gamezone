#!/usr/bin/env python
"""
Test script to verify email sending functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamezone.settings')
django.setup()

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def test_email_sending():
    """Test email sending functionality"""
    print("Testing email sending...")
    
    # Test email configuration
    print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    print(f"DEFAULT_FROM_EMAIL: {settings.DEFAULT_FROM_EMAIL}")
    
    # Test email content
    subject = 'Test Email from GameZone'
    message = 'This is a test email to verify email sending works.'
    
    html_message = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Email</title>
    </head>
    <body>
        <h1>Test Email from GameZone</h1>
        <p>This is a test email to verify email sending works.</p>
        <p>If you receive this email, the email configuration is working correctly!</p>
    </body>
    </html>
    '''
    
    try:
        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            ['test@example.com']  # Replace with your email for testing
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        print("✅ Email sent successfully!")
        print("Check your email inbox for the test message.")
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        print("Please check your email configuration in settings.py")

if __name__ == '__main__':
    test_email_sending() 