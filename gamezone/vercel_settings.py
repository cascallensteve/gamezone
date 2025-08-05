from .settings import *

# Vercel-specific settings
DEBUG = False
ALLOWED_HOSTS = ['*', '.vercel.app', '.now.sh']

# Static files configuration for Vercel
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Database configuration for Vercel
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
} 