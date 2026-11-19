#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "=== [JustBaddo] Starting Render Build ==="

# Upgrade pip
python -m pip install --upgrade pip

# Install baseline and production dependencies
pip install -r requirements.txt -r requirements-prod.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate --no-input

# Seed verified discography catalogue and baseline milestones
python manage.py seed_catalogue

echo "=== [JustBaddo] Build Completed Successfully ==="
