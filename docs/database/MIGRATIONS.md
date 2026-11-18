# JUSTBADDO — DATABASE MIGRATIONS GUIDE

## 1. Overview & Principles

In JustBaddo, database schema evolution is managed strictly through **Django Migrations** backed by **PostgreSQL**.

### Core Migration Principles
1. **Source of Truth in Code**: Python model definitions in each Django application represent the sole authoritative declaration of the database schema.
2. **Deterministic & Version-Controlled**: Every change to database structure (tables, fields, foreign keys, constraints, indexes) is captured as a versioned migration file committed to Git.
3. **Reproducibility**: Any fresh environment (local development, CI test runner, staging, production) can recreate the entire schema from scratch using `python manage.py migrate`.
4. **Data Safety**: Schema changes must preserve existing data integrity. Destructive operations (dropping columns, changing types) require explicit backward-compatible transitions.

---

## 2. Migration Architecture & Current State

All 10 domain applications plus the core application maintain their own `migrations/` directory:

| Application | Initial Migration | Models Covered | Dependencies |
|---|---|---|---|
| `core` | None (Abstract base only) | `TimeStampedModel` | None |
| `accounts` | `0001_initial.py` | `UserProfile`, `AccountSettings` | `auth` |
| `music` | `0001_initial.py` | `Artist`, `Genre`, `Album`, `Track`, `TimelineMilestone` | None |
| `playback` | `0001_initial.py` | `PlaybackSession`, `ListeningHistory` | `auth`, `music` |
| `playlists` | `0001_initial.py` | `Playlist`, `PlaylistTrack` | `auth`, `music` |
| `community` | `0001_initial.py` | `Post`, `Comment`, `PostLike`, `Follow` | `auth` |
| `arena` | `0001_initial.py` | `Poll`, `PollOption`, `PollVote`, `SongBattle`, `BattleVote`, `TriviaQuestion`, `TriviaSubmission` | `auth`, `music` |
| `stories` | `0001_initial.py` | `Story` | `auth` |
| `notifications` | `0001_initial.py` | `Notification` | `auth` |
| `licensing` | `0001_initial.py` | `RightsRecord`, `RightsInquiry` | `auth`, `music` |
| `moderation` | `0001_initial.py` | `Report`, `ModerationAction`, `UserRestriction` | `auth` |

---

## 3. Standard Migration Workflow

### Step 1: Modify Models
Edit `models.py` in the appropriate app directory (e.g. adding a new field or index to `music/models.py`).

### Step 2: Generate Migration
Run the Django migration generator:
```bash
python manage.py makemigrations
```
To generate migrations for a specific application:
```bash
python manage.py makemigrations music
```
*Always inspect the newly generated file in `<app>/migrations/` to verify operations.*

### Step 3: Inspect Generated SQL
Before applying to PostgreSQL, inspect the raw SQL statements generated:
```bash
python manage.py sqlmigrate <app_name> <migration_number>
# Example:
python manage.py sqlmigrate music 0001
```

### Step 4: Apply Migrations
Apply unapplied migrations to the target PostgreSQL database:
```bash
python manage.py migrate
```

### Step 5: Verify Migration Status
Check applied vs pending migrations:
```bash
python manage.py showmigrations
```
Applied migrations are denoted with `[X]`; pending migrations are denoted with `[ ]`.

---

## 4. Zero-Downtime Migration Guidelines

To maintain 100% uptime and avoid locking issues in production PostgreSQL environments, adhere to the following rules:

### 1. Adding New Columns
- **Always provide a default or allow null (`null=True`)**:
  ```python
  # Safe:
  tagline = models.CharField(max_length=255, blank=True, default='')
  featured_date = models.DateField(null=True, blank=True)
  ```
- In PostgreSQL 11+, `ADD COLUMN ... DEFAULT` is a constant-time metadata operation and does not rewrite the table.

### 2. Renaming Columns
- Never perform a direct in-place rename on high-traffic tables during peak hours, as it causes application race conditions between deployment of old code and new schema.
- **Three-Phase Strategy (Expand/Contract)**:
  1. Add the new column with new name.
  2. Write to both old and new columns in application code; backfill historical data.
  3. Switch reads to new column, then deprecate and remove old column in a later release.

### 3. Adding Indexes
- For large tables in production, use `CONCURRENTLY` to avoid write locks:
  ```python
  from django.contrib.postgres.indexes import ConcurrentAddIndexOperation
  ```
  Django requires `atomic = False` on the Migration class when using `ConcurrentAddIndexOperation`.

### 4. Modifying Foreign Keys & Cascades
- Avoid changing `on_delete` behaviors without reviewing the volume of child records. Ensure foreign keys have indexing on child tables (Django adds this automatically for `ForeignKey`).

---

## 5. Rollback and Reversal Procedures

If a migration must be reverted, Django allows rolling back to any preceding migration state.

### Reverting to a Specific Migration
To roll back an application to a prior migration:
```bash
python manage.py migrate <app_name> <target_migration_number>
# Example: Roll back music app to initial state:
python manage.py migrate music 0001
```

### Unapplying All Migrations for an App
To unapply all migrations for an application (dropping its tables):
```bash
python manage.py migrate <app_name> zero
```
> [!CAUTION]
> Running `migrate <app_name> zero` drops the tables for that application, permanently deleting all table data. Ensure a backup exists prior to running rollback commands in production.

### Reverting Failed Migration Files
1. Roll back the database state using `python manage.py migrate <app_name> <prior_migration>`.
2. Delete the unwanted migration file from `<app>/migrations/`.
3. Adjust `models.py` back to the desired code state.

---

## 6. Data Migrations & Seeding

For structural data population or transformations, use custom data migrations or Django management commands:

### Using the Catalogue Seeder
To repopulate or verify catalogue data:
```bash
python manage.py seed_catalogue
```
The `seed_catalogue` command is idempotent (`get_or_create`), ensuring it can be executed safely multiple times without creating duplicate records.

### Creating Data Migrations
For migration scripts that modify existing data rows:
```bash
python manage.py makemigrations <app_name> --empty -n populate_default_genres
```
In the generated migration:
```python
def populate_genres(apps, schema_editor):
    Genre = apps.get_model('music', 'Genre')
    Genre.objects.get_or_create(name='Indigenous Hip-hop', slug='indigenous-hip-hop')

class Migration(migrations.Migration):
    dependencies = [('music', '0001_initial')]
    operations = [
        migrations.RunPython(populate_genres, reverse_code=migrations.RunPython.noop),
    ]
```

---

## 7. Migration CI/CD Integration

In CI pipelines, verify migrations before merging:
1. **Check for missing migrations**:
   ```bash
   python manage.py makemigrations --check --dry-run
   ```
   Exits with non-zero code if model changes were made without generating migrations.
2. **Execute test migrations**:
   ```bash
   python manage.py migrate --noinput
   ```
3. **Execute automated test suite**:
   ```bash
   python manage.py test
   ```
