#!/usr/bin/env bash
# ==============================================================================
# JustBaddo - Production Zero-Downtime Deployment Script
# Steps: git pull, dependency check, database migrate, collectstatic, gunicorn reload
# ==============================================================================

set -euo pipefail

APP_DIR="${APP_DIR:-/var/www/justbaddo}"
VENV_DIR="${APP_DIR}/.venv"

echo "=============================================================================="
echo "Starting JustBaddo Production Deployment: $(date '+%Y-%m-%d %H:%M:%S')"
echo "=============================================================================="

cd "${APP_DIR}"

# 1. Update source code
echo "[Step 1/5] Pulling latest production release from Git..."
git fetch origin main
git merge origin/main --ff-only

# 2. Update Python dependencies
echo "[Step 2/5] Installing/verifying production Python requirements..."
"${VENV_DIR}/bin/pip" install --upgrade pip
"${VENV_DIR}/bin/pip" install -r requirements-prod.txt

# 3. Apply PostgreSQL migrations
echo "[Step 3/5] Applying database migrations..."
"${VENV_DIR}/bin/python" manage.py migrate --noinput

# 4. Collect and compress static assets
echo "[Step 4/5] Collecting and optimizing static files..."
"${VENV_DIR}/bin/python" manage.py collectstatic --noinput

# 5. Reload application WSGI workers
echo "[Step 5/5] Gracefully reloading Gunicorn workers..."
if systemctl is-active --quiet justbaddo.service; then
    systemctl reload justbaddo.service
    echo "Reload signal sent to justbaddo.service."
elif command -v docker >/dev/null 2>&1 && docker ps | grep -q justbaddo_prod_web; then
    docker compose -f docker-compose.prod.yml restart web
    echo "Restarted web container via docker compose."
fi

# 6. Verify health status
echo "Verifying application health..."
sleep 2
if curl -sf http://127.0.0.1:8000/api/v1/health/ >/dev/null; then
    echo "Deployment successful! JustBaddo is operational and healthy."
else
    echo "WARNING: Health check failed! Inspect logs in ${APP_DIR}/logs/"
    exit 1
fi
