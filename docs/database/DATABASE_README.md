# JUSTBADDO — DATABASE README

## 1. Overview

The JustBaddo database layer provides the relational, persistent data foundation powering the entire platform. Designed during Phase 3 (Database Development), it connects Django models and the Django ORM to a production-grade **PostgreSQL** relational database.

JustBaddo is an independent music discovery and fan community platform dedicated to Olamide Baddo. The database is architected to support:
- Verified Olamide music discography (studio albums, EPs, singles, tracks, milestones, credits).
- User accounts, profiles, preferences, and activity tracking.
- Curated and personal playlists with explicit track ordering.
- Community discussions, nested comments, like reactions, and social following.
- Interactive Fan Arena modules (live polls, single elimination song battles, trivia leaderboards).
- Curated and moderated fan stories.
- In-app notification delivery and read-state management.
- Zero-copyright compliance, licensing records, territory allowances, and external provider references.
- Content reporting, moderation review workflows, and user restrictions.

---

## 2. Technology Stack & Database Engine

| Layer | Technology | Details |
|---|---|---|
| **RDBMS** | PostgreSQL 18 | ACID-compliant relational database engine |
| **Database Driver** | `psycopg2-binary` (v2.9.13) | C-optimized PostgreSQL adapter for Python |
| **ORM / Migration Engine** | Django ORM (Django 6.1.3) | Declarative relational modeling & migrations |
| **Configuration** | `python-dotenv` (v1.2.4) | 12-Factor environment variable management |
| **Catalog Seeder** | Custom Django Management Command | `python manage.py seed_catalogue` |
| **Backup Utilities** | `pg_dump` & `pg_restore` | Custom archive format (`.dump`) with integrity verification |

---

## 3. Database Architecture & Installed Applications

The database layer mirrors the 11 modular Django applications:

```
[auth_user] <1:1> [accounts_user_profile]
     |      <1:1> [accounts_user_settings]
     |      <1:1> [moderation_user_restrictions]
     |
     +------------< [community_posts] <1:N> [community_comments]
     |                    ^
     |                    +---< [community_post_likes]
     |
     +------------< [playlists_playlists] <1:N> [playlists_playlist_tracks] >---+
     |                                                                          |
     +------------< [arena_poll_votes] >--- [arena_poll_options] >- [arena_polls]
     |                                                                          |
     +------------< [arena_battle_votes] >- [arena_song_battles] >--------------+
     |                                                                          |
     +------------< [stories_stories]                                           |
     |                                                                          |
     +------------< [notifications_notifications]                               |
     |                                                                          |
     +------------< [playback_listening_history] >------------------------------+
                                                                                |
                                                                                v
                       [music_albums] <1:N> [music_tracks] <1:1> [licensing_rights_records]
                             |                     ^
                             v                     |
                   [music_albums_genres]    [music_artists]
```

### Domain Models Summary

1. **`accounts`**:
   - `UserProfile`: Extended profile attributes (display name, bio, Bariga badge, favorite era/album/song, avatar).
   - `AccountSettings`: Privacy and notification toggles (`email_notifications`, `public_profile`, `show_listening_history`).
2. **`music`**:
   - `Artist`: Artist profile, primary genres, verified artist badge.
   - `Genre`: Standardized genres (Indigenous Hip-hop, Afrobeats, Street-hop).
   - `Album`: Studio albums, EPs, release years, cover artwork URLs, discography order.
   - `Track`: Audio metadata, duration, track number, external stream URLs, authorized stream status.
   - `TimelineMilestone`: Career timeline entries from 2010 to present.
3. **`playback`**:
   - `PlaybackSession`: Ephemeral or active playback token tracking.
   - `ListeningHistory`: Historical record of tracks played per user with completion timestamps.
4. **`playlists`**:
   - `Playlist`: User-created and curated platform playlists with cover images and visibility.
   - `PlaylistTrack`: Intermediary through-model with explicit `order` index and `(playlist, track)` uniqueness.
5. **`community`**:
   - `Post`: Editorial announcements and user discussion posts.
   - `Comment`: User comments on community posts.
   - `PostLike`: Like relation with unique `(post, user)` constraint.
   - `Follow`: Social graph tracking `(follower, following)` pairs.
6. **`arena`**:
   - `Poll`: Community voting topics with expiration timestamps.
   - `PollOption`: Choices per poll with vote counters.
   - `PollVote`: One-vote-per-user constraint `(poll, user)`.
   - `SongBattle`: Head-to-head track contests (`track_a` vs `track_b`).
   - `BattleVote`: One-vote-per-user constraint `(battle, user)`.
   - `TriviaQuestion`: Discography trivia bank with four choices and explanation.
   - `TriviaSubmission`: User answer submission and score tracking.
7. **`stories`**:
   - `Story`: Long-form fan essays, memories, and concert experiences with moderation workflows (`PENDING`, `APPROVED`, `REJECTED`).
8. **`notifications`**:
   - `Notification`: In-app event alerts (likes, comments, battle results) with read timestamps.
9. **`licensing`**:
   - `RightsRecord`: Explicit licensing metadata per track, territorial limits, authorized external platform URLs (Audiomack, YouTube, Spotify).
   - `RightsInquiry`: Inbound licensing queries and compliance requests.
10. **`moderation`**:
    - `Report`: Flagged content (posts, comments, stories) with status workflow (`PENDING`, `REVIEWED`, `DISMISSED`, `ACTION_TAKEN`).
    - `ModerationAction`: Audit log of administrative actions taken by staff.
    - `UserRestriction`: User penalty records (warnings, mutes, temporary suspensions, permanent bans).

---

## 4. Environment Configuration

Database connection settings are loaded through `.env` in the project root:

```env
POSTGRES_DB=justbaddo_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=root
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

In `config/settings.py`, Django reads these variables using `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'justbaddo_db'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'root'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'CONN_MAX_AGE': 600,
    }
}
```

---

## 5. Quick Start & Common Database Operations

### Run Database Migrations
Apply all unapplied schema migrations to PostgreSQL:
```bash
python manage.py migrate
```

### Seed Verified Catalogue & Demo Data
Populate the database with verified Olamide albums, tracks, career milestones, and demo records:
```bash
python manage.py seed_catalogue
```

### Create a Superuser for Django Admin
```bash
python manage.py createsuperuser
```

### Access Django Admin Portal
Start the development server and navigate to `http://localhost:8000/admin/`:
```bash
python manage.py runserver
```

---

## 6. Verification and Test Suite

All 46 automated backend tests run against the PostgreSQL database engine using `JustBaddoTestCase` (`core/test_base.py`), which loads the verified catalogue into the test database:

```bash
python manage.py test
```
Result:
```text
Ran 46 tests in 115.417s
OK
```

---

## 7. Documentation Index

For detailed architectural specifications, full schema listings, migration management, and disaster recovery procedures, refer to:
- [DATABASE_ARCHITECTURE.md](file:///c:/Users/USER/Documents/JustBaddo/docs/database/DATABASE_ARCHITECTURE.md) — Architectural overview, data flows, indexing strategy, and relationships.
- [DATABASE_SCHEMA.md](file:///c:/Users/USER/Documents/JustBaddo/docs/database/DATABASE_SCHEMA.md) — Comprehensive table-by-table schema specification, column types, constraints, and defaults.
- [MIGRATIONS.md](file:///c:/Users/USER/Documents/JustBaddo/docs/database/MIGRATIONS.md) — Migration creation, deployment workflow, zero-downtime rules, and rollback procedures.
- [BACKUP_AND_RECOVERY.md](file:///c:/Users/USER/Documents/JustBaddo/docs/database/BACKUP_AND_RECOVERY.md) — Disaster recovery runbook, `pg_dump`/`pg_restore` commands, and verified restoration test logs.
