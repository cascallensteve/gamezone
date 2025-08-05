#!/bin/bash
# Build script for Render deployment with Railway database

# Upgrade pip to latest version
pip install --upgrade pip

# Install system dependencies for Pillow
apt-get update && apt-get install -y \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    libwebp-dev \
    libtiff5-dev \
    libopenjp2-7-dev

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations to Railway PostgreSQL
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput

# Test database connection
python manage.py check --database default 