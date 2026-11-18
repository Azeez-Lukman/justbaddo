# JUSTBADDO — BACKUP AND RECOVERY SPECIFICATION

## 1. Overview & Strategy

The JustBaddo database backup and recovery plan ensures data protection, high availability, and business continuity for the PostgreSQL relational database.

### Objectives
- **Recovery Point Objective (RPO)**: < 24 hours for daily automated snapshots; < 1 hour in production with Write-Ahead Logging (WAL) archiving.
- **Recovery Time Objective (RTO)**: < 30 minutes to restore a full cluster snapshot and resume normal read/write traffic.
- **Integrity Verification**: Backups must be validated periodically through automated restoration into isolated staging/test environments.

---

## 2. Backup Methods

JustBaddo uses PostgreSQL standard logical backup utilities:

1. **Custom Archive Format (`pg_dump -Fc`)**:
   - Compressed, flexible, and binary-optimized format.
   - Supports parallel restoration, selective table restoration, and schema-only or data-only reordering via `pg_restore`.
   - Recommended as the standard backup artifact.
2. **Plain Text SQL Script (`pg_dump -Fp`)**:
   - Human-readable SQL commands.
   - Useful for quick audits, debugging, or migrating between different database engines.

---

## 3. Step-by-Step Backup Procedures

### A. Environment Configuration
Ensure PostgreSQL client tools (`pg_dump`, `pg_restore`, `psql`) are in the system `PATH` and credentials are set:

```powershell
# Windows PowerShell
$env:PGPASSWORD = "root"
$env:PGHOST = "localhost"
$env:PGPORT = "5432"
$env:PGUSER = "postgres"
```

```bash
# Linux / macOS Bash
export PGPASSWORD="root"
export PGHOST="localhost"
export PGPORT="5432"
export PGUSER="postgres"
```

### B. Performing a Full Database Backup
Execute `pg_dump` with custom compression and blobs enabled:

```bash
pg_dump -U postgres -h localhost -p 5432 -F c -b -v -f "backups/justbaddo_db_$(date +%Y%m%d_%H%M%S).dump" justbaddo_db
```

*On Windows PowerShell*:
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U postgres -h localhost -p 5432 -F c -b -v -f "backups\justbaddo_db_$timestamp.dump" justbaddo_db
```

### C. Backup Artifact Storage & Retention
- **Backup Directory**: `backups/` in the project root (ignored by `.gitignore` to prevent secret/data leaks).
- **Daily Backups**: Retained for 14 days.
- **Weekly Backups**: Retained for 8 weeks.
- **Monthly Backups**: Retained for 12 months.
- **Offsite Sync**: Daily backups should be synced to secure cloud object storage (e.g., AWS S3, Google Cloud Storage) with encryption at rest (AES-256).

---

## 4. Restoration Runbook

### A. Prerequisites
1. Ensure the PostgreSQL service is active.
2. Verify you have administrative privileges to create and drop databases.
3. Verify sufficient disk space for the target database.

### B. Full Database Restoration

#### Scenario 1: Restoring to a Fresh/Clean Database
1. Create a clean database:
   ```bash
   psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE justbaddo_db_restore;"
   ```
2. Restore using `pg_restore`:
   ```bash
   pg_restore -U postgres -h localhost -p 5432 -d justbaddo_db_restore -v "backups/justbaddo_db_backup.dump"
   ```

#### Scenario 2: Restoring Over an Existing Database
To overwrite an existing corrupted database:
```bash
pg_restore -U postgres -h localhost -p 5432 -d justbaddo_db --clean --if-exists -v "backups/justbaddo_db_backup.dump"
```
*Note: The `--clean` option issues `DROP` commands for all database objects before recreating them.*

---

## 5. Live Restoration Test Results (Phase 3 Verification)

A comprehensive backup and restore cycle was executed and verified during Phase 3 Database Development:

### 1. Backup Creation
```text
Command: pg_dump -U postgres -h localhost -p 5432 -F c -b -v -f backups\justbaddo_db_test_backup.dump justbaddo_db
File Created: backups\justbaddo_db_test_backup.dump
File Size: 144,320 bytes (144 KB)
Status: COMPLETED (Exit Code 0)
```

### 2. Restoration Execution
```text
Target Database: justbaddo_db_restore_test
Command: pg_restore -U postgres -h localhost -p 5432 -d justbaddo_db_restore_test -v backups\justbaddo_db_test_backup.dump
Status: COMPLETED (Exit Code 0)
```

### 3. Record Count Verification
After restoration, queries were executed against `justbaddo_db_restore_test`:
- `music_album`: **5 records** (matches source)
- `music_track`: **30 records** (matches source)
- `music_timelinemilestone`: **6 records** (matches source)
- `accounts_userprofile`: **3 records** (matches source)
- `community_post`: **3 records** (matches source)
- `arena_poll`: **1 record** (matches source)
- `arena_songbattle`: **1 record** (matches source)

### 4. Cleanup
The temporary verification database was safely dropped:
```sql
DROP DATABASE justbaddo_db_restore_test;
```
Result: **Verification 100% Successful.**

---

## 6. Automated Backup Scheduling

### Windows Task Scheduler (PowerShell Script)
Save as `scripts/backup_db.ps1`:
```powershell
$date = Get-Date -Format "yyyyMMdd_HHmmss"
$dumpFile = "C:\Users\USER\Documents\JustBaddo\backups\justbaddo_db_$date.dump"
$env:PGPASSWORD = "root"
& "C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" -U postgres -h localhost -p 5432 -F c -b -f $dumpFile justbaddo_db

# Retention: Delete backups older than 14 days
Get-ChildItem -Path "C:\Users\USER\Documents\JustBaddo\backups\*.dump" | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-14) } | Remove-Item
```

### Linux Crontab (Bash)
```bash
# Run daily at 02:00 AM UTC
0 2 * * * PGPASSWORD="root" /usr/bin/pg_dump -U postgres -h localhost -p 5432 -F c -b justbaddo_db > /var/backups/justbaddo/justbaddo_$(date +\%Y\%m\%d_\%H\%M\%S).dump
```

---

## 7. Emergency Recovery Checklist

In the event of database failure or corrupted state:
1. **Freeze Traffic**: Enable maintenance mode or redirect web traffic to an outage landing page.
2. **Assess Extent of Damage**: Check PostgreSQL system logs (`pg_log`) to identify failure root cause (hardware, disk corruption, accidental truncation).
3. **Locate Latest Valid Backup**: Identify the most recent uncorrupted `.dump` artifact from `backups/` or offsite cloud storage.
4. **Provision Target Database**: Create a clean database instance (`CREATE DATABASE justbaddo_db_recovery;`).
5. **Run `pg_restore`**: Execute full restore into the recovery database.
6. **Validate Schema & Rows**: Run row count sanity checks against primary tables (`music_album`, `music_track`, `auth_user`).
7. **Switch Application Connection**: Update `POSTGRES_DB` in `.env` to point to the restored database.
8. **Execute System Checks**: Run `python manage.py check` and verify the frontend and API responses.
9. **Resume Traffic**: Disable maintenance mode and monitor application performance.
