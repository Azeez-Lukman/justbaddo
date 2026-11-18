#!/usr/bin/env bash
# ==============================================================================
# JustBaddo - Production Automated PostgreSQL Backup Script
# Creates a compressed, custom-format dump with SHA256 checksum and retention prune.
# ==============================================================================

set -euo pipefail

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backups}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_NAME="${POSTGRES_DB:-justbaddo_db}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"

BACKUP_FILE="${BACKUP_DIR}/justbaddo_db_${TIMESTAMP}.dump"
CHECKSUM_FILE="${BACKUP_FILE}.sha256"

# Ensure backup directory exists
mkdir -p "${BACKUP_DIR}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting production database backup: ${DB_NAME}..."

# Execute pg_dump in custom compressed format (-Fc)
PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_dump \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${DB_NAME}" \
    -Fc \
    --blobs \
    --verbose \
    -f "${BACKUP_FILE}"

# Generate SHA256 integrity checksum
if command -v sha256sum >/dev/null 2>&1; then
    sha256sum "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
elif command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "${BACKUP_FILE}" > "${CHECKSUM_FILE}"
fi

FILE_SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup complete: ${BACKUP_FILE} (${FILE_SIZE})"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Checksum recorded: ${CHECKSUM_FILE}"

# Retention Policy: Prune backups older than 14 days
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applying 14-day retention cleanup..."
find "${BACKUP_DIR}" -name "justbaddo_db_*.dump" -mtime +14 -exec rm -f {} \;
find "${BACKUP_DIR}" -name "justbaddo_db_*.sha256" -mtime +14 -exec rm -f {} \;
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Retention prune complete."
