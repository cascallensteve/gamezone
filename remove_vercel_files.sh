#!/bin/bash
# Remove Vercel-specific files for Render deployment

# Remove Vercel configuration
rm -f vercel.json

# Remove Vercel-specific settings
rm -f gamezone/vercel_settings.py

# Update WSGI file to remove Vercel-specific code 