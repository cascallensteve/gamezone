#!/bin/bash
# Build script for Render deployment with Railway database

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations to Railway PostgreSQL
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput

# Test database connection
python manage.py check --database default 