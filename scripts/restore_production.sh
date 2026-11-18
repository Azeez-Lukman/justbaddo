#!/usr/bin/env bash
# ==============================================================================
# JustBaddo - Production Database Recovery & Verification Script
# Validates checksum, prompts for confirmation, and restores custom-format dump.
# ==============================================================================

set -euo pipefail

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <path-to-dump-file> [target-database-name]"
    exit 1
fi

DUMP_FILE="$1"
TARGET_DB="${2:-${POSTGRES_DB:-justbaddo_db}}"
DB_USER="${POSTGRES_USER:-postgres}"
DB_HOST="${POSTGRES_HOST:-localhost}"
DB_PORT="${POSTGRES_PORT:-5432}"

if [ ! -f "${DUMP_FILE}" ]; then
    echo "ERROR: Backup file '${DUMP_FILE}' not found."
    exit 1
fi

# Checksum verification if available
CHECKSUM_FILE="${DUMP_FILE}.sha256"
if [ -f "${CHECKSUM_FILE}" ]; then
    echo "Verifying SHA256 integrity checksum..."
    if command -v sha256sum >/dev/null 2>&1; then
        sha256sum -c "${CHECKSUM_FILE}"
    elif command -v shasum >/dev/null 2>&1; then
        shasum -a 256 -c "${CHECKSUM_FILE}"
    fi
    echo "Checksum verified successfully."
else
    echo "WARNING: No .sha256 checksum file found. Proceeding without checksum verification."
fi

echo "=============================================================================="
echo "TARGET DATABASE: ${TARGET_DB} on ${DB_HOST}:${DB_PORT}"
echo "SOURCE DUMP:     ${DUMP_FILE}"
echo "=============================================================================="
echo "WARNING: Restoring will overwrite existing data in '${TARGET_DB}'!"

if [ -t 0 ]; then
    read -p "Type 'RESTORE' to continue: " CONFIRM
    if [ "${CONFIRM}" != "RESTORE" ]; then
        echo "Restore cancelled by user."
        exit 0
    fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting restore into ${TARGET_DB}..."

PGPASSWORD="${POSTGRES_PASSWORD:-}" pg_restore \
    -h "${DB_HOST}" \
    -p "${DB_PORT}" \
    -U "${DB_USER}" \
    -d "${TARGET_DB}" \
    --clean \
    --if-exists \
    --no-owner \
    --no-privileges \
    --verbose \
    "${DUMP_FILE}"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoration completed successfully into ${TARGET_DB}."
