# JUSTBADDO — REST API DOCUMENTATION (v1)

Base URL: `/api/v1/` (alias `/api/`)

---

## Table of Contents
1. [Core & System](#1-core--system)
2. [Accounts & Profiles](#2-accounts--profiles)
3. [Music Catalogue](#3-music-catalogue)
4. [Playback Management](#4-playback-management)
5. [Playlists](#5-playlists)
6. [Community Discussions](#6-community-discussions)
7. [Fan Arena](#7-fan-arena)
8. [Fan Stories](#8-fan-stories)
9. [Notifications](#9-notifications)
10. [Licensing & Rights](#10-licensing--rights)
11. [Moderation](#11-moderation)

---

## 1. Core & System

### System Health Check
- **Endpoint:** `GET /api/v1/health/`
- **Auth Required:** None
- **Response:**
  ```json
  {
    "status": "success",
    "message": "JustBaddo backend operational.",
    "data": {
      "status": "healthy",
      "service": "justbaddo-backend",
      "version": "1.0.0-phase2",
      "environment": "development",
      "database_engine": "sqlite3"
    }
  }
  ```

### Platform Metadata
- **Endpoint:** `GET /api/v1/platform/`
- **Auth Required:** None
- **Response:** Brand identity, artist profile, active phase, and legal disclaimer.

---

## 2. Accounts & Profiles

### Register Account
- **Endpoint:** `POST /api/v1/accounts/register/`
- **Auth Required:** None
- **Request Body:**
  ```json
  {
    "username": "newuser",
    "email": "user@domain.com",
    "password": "SecurePassword123!",
    "agree_terms": true,
    "fav_era": "Carpe Diem (2020)"
  }
  ```
- **Response:** HTTP 201 Created with provisioned fan profile object.

### Login
- **Endpoint:** `POST /api/v1/accounts/login/`
- **Auth Required:** None
- **Request Body:**
  ```json
  {
    "username_or_email": "baddofan99",
    "password": "Password123!"
  }
  ```
- **Response:** HTTP 200 OK with authenticated user profile and session cookie.

### Logout
- **Endpoint:** `POST /api/v1/accounts/logout/`
- **Auth Required:** None (clears session if present)
- **Response:** HTTP 200 OK.

### Current User Profile
- **Endpoint:** `GET /api/v1/accounts/profile/` | `PATCH /api/v1/accounts/profile/`
- **Auth Required:** Optional (defaults to active user or demo fallback)
- **Patch Body:** `{"display_name": "...", "bio": "...", "city": "...", "favorite_era": "..."}`

### Public Profile by Username
- **Endpoint:** `GET /api/v1/accounts/users/{username}/`
- **Auth Required:** None (respects `is_profile_public` flag and masks private fields for unauthenticated visitors)

### Members Directory
- **Endpoint:** `GET /api/v1/accounts/members/`
- **Auth Required:** None (public member discovery)
- **Query Params:**
  - `q`: Search username, display name, bio, city, country
  - `tier`: Filter by membership tier (`Explorer`, `Gold Fan`, `Platinum VIP`, `VIP Archival Member`)
  - `badge`: Filter by badge slug
  - `ordering`: `reputation` (default), `date_joined`, `username`
  - `page`: Page number (default: 1)
  - `page_size`: Page size (default: 20, max: 100)

### Badges Catalogue
- **Endpoint:** `GET /api/v1/accounts/badges/`
- **Auth Required:** None
- **Response:** List of all official fan badges with slug, name, description, tier, icon name, points value, and recipient count.

### Accept Community Guidelines
- **Endpoint:** `POST /api/v1/accounts/guidelines/accept/`
- **Auth Required:** Required
- **Response:** HTTP 200 OK with `accepted_community_guidelines: true`.

### Delete / Deactivate Account
- **Endpoint:** `POST /api/v1/accounts/delete/`
- **Auth Required:** Required
- **Request Body:** `{"password": "CurrentPassword123!", "reason": "Optional reason"}`
- **Response:** HTTP 200 OK with account deactivated and session invalidated.

### Account Settings
- **Endpoint:** `GET /api/v1/accounts/settings/` | `PATCH /api/v1/accounts/settings/`
- **Patch Body:** `{"auto_advance_queue": true, "audio_preview_enabled": true, ...}`

---

## 3. Music Catalogue

### Artist Biography & Summary
- **Endpoint:** `GET /api/v1/music/artist/`
- **Auth Required:** None

### List Albums & EPs
- **Endpoint:** `GET /api/v1/music/albums/`
- **Query Params:**
  - `type`: `Studio Album` | `EP`
  - `q`: Search keyword
  - `sort`: `year_desc` | `year_asc` | `title`
- **Response:** List of albums with track counts, labels, artwork URLs, and credits.

### Album Detail & Tracklist
- **Endpoint:** `GET /api/v1/music/albums/{slug}/`
- **Auth Required:** None
- **Response:** Full release metadata, complete tracks array, producer credits, and BPM/key tags.

### List Singles & Major Collaborations
- **Endpoint:** `GET /api/v1/music/singles/`
- **Query Params:** `q` (filter title or featured artists)

### Track Detail
- **Endpoint:** `GET /api/v1/music/tracks/{track_id}/`
- **Auth Required:** None
- **Response:** Technical details (BPM, Key, Producer, Release Year, Rights Notice, Playback Status).

### Unified Catalogue Search
- **Endpoint:** `GET /api/v1/music/search/?q={query}`
- **Response:** Matches split into `albums`, `tracks`, and `singles`.

### Career Timeline
- **Endpoint:** `GET /api/v1/music/timeline/`
- **Response:** Chronological milestones from 2010 to present with archival citations.

---

## 4. Playback Management

### Track Playback Availability Check
- **Endpoint:** `GET /api/v1/playback/check/{track_id}/?territory=NG`
- **Auth Required:** None
- **Response:**
  ```json
  {
    "status": "success",
    "data": {
      "exists": true,
      "track_id": "iki-01",
      "title": "Metaverse",
      "can_play": true,
      "status": "JUSTBADDO_STREAMING",
      "provider": "web_audio_synth",
      "territory": "NG",
      "is_synthetic_preview": true
    }
  }
  ```

### Initialize Playback Session
- **Endpoint:** `POST /api/v1/playback/session/`
- **Request Body:** `{"track_id": "iki-01", "client_provider": "mock_synth"}`
- **Response:** HTTP 201 Created with `session_id`, or HTTP 403 Forbidden if rights are restricted.

### Log Playback Progress
- **Endpoint:** `POST /api/v1/playback/log/`
- **Request Body:** `{"track_id": "iki-01", "duration_seconds": 120, "completed_listen": true}`

### Listening History
- **Endpoint:** `GET /api/v1/playback/history/`

---

## 5. Playlists

### List Playlists
- **Endpoint:** `GET /api/v1/playlists/`
- **Response:** Array of editorial playlists and visible user collections.

### Create Playlist
- **Endpoint:** `POST /api/v1/playlists/`
- **Request Body:** `{"title": "...", "description": "...", "is_private": false}`

### Playlist Detail
- **Endpoint:** `GET /api/v1/playlists/{playlist_id}/`
- **Response:** Playlist metadata and full embedded tracks list.

### Edit / Delete Playlist
- **Endpoint:** `PATCH /api/v1/playlists/{playlist_id}/` | `DELETE /api/v1/playlists/{playlist_id}/`

### Add Track to Playlist
- **Endpoint:** `POST /api/v1/playlists/{playlist_id}/tracks/`
- **Request Body:** `{"track_id": "iki-01"}`

### Remove Track from Playlist
- **Endpoint:** `DELETE /api/v1/playlists/{playlist_id}/tracks/{track_id}/`

---

## 6. Community Discussions

### List Discussion Posts
- **Endpoint:** `GET /api/v1/community/posts/`
- **Query Params:**
  - `category`: `Discography` | `Lyrics & Meaning` | `Concerts & OLIC` | `General Fan Chat`
  - `q`: Search keyword

### Create Post
- **Endpoint:** `POST /api/v1/community/posts/`
- **Request Body:** `{"title": "...", "category": "Discography", "content": "..."}`

### Post Detail with Comments
- **Endpoint:** `GET /api/v1/community/posts/{post_id}/`
- **Response:** Threaded replies, timestamps, author details, and like counts.

### Add Comment / Reply
- **Endpoint:** `POST /api/v1/community/posts/{post_id}/comments/`
- **Request Body:** `{"content": "..."}`

### Toggle Post Like
- **Endpoint:** `POST /api/v1/community/posts/{post_id}/like/`

---

## 7. Fan Arena

### List Active Polls
- **Endpoint:** `GET /api/v1/arena/polls/`
- **Response:** Poll questions, vote tallies, and percentage distributions.

### Vote on Poll
- **Endpoint:** `POST /api/v1/arena/polls/{poll_id}/vote/`
- **Request Body:** `{"option_id": "opt-01"}`

### List Song Battles
- **Endpoint:** `GET /api/v1/arena/battles/`

### Vote on Song Battle
- **Endpoint:** `POST /api/v1/arena/battles/{battle_id}/vote/`
- **Request Body:** `{"selected_song": "song_a" | "song_b"}`

### Retrieve Trivia Questions
- **Endpoint:** `GET /api/v1/arena/trivia/`
- **Response:** Questions and option arrays (correct answers stripped for integrity).

### Submit Trivia Sheet
- **Endpoint:** `POST /api/v1/arena/trivia/submit/`
- **Request Body:** `{"answers": {"q1": 1, "q2": 1, ...}}`
- **Response:** Score breakdown, awarded points, percentage, and historical explanations.

### Fan Leaderboard
- **Endpoint:** `GET /api/v1/arena/leaderboard/`
- **Response:** Top fan rankings with points, badges, and prestige tiers.

---

## 8. Fan Stories

### List Stories
- **Endpoint:** `GET /api/v1/stories/`
- **Response:** Published editorial fan reflections and concert memories.

### Story Detail
- **Endpoint:** `GET /api/v1/stories/{story_id}/`
- **Response:** Full essay HTML content, author credentials, read time, and cover art.

### Submit Story for Review
- **Endpoint:** `POST /api/v1/stories/submit/`
- **Request Body:** `{"title": "...", "content": "...", "read_time": "5 min read", "tags": "..."}`

---

## 9. Notifications

### List Notifications
- **Endpoint:** `GET /api/v1/notifications/?unread_only=true`

### Unread Count
- **Endpoint:** `GET /api/v1/notifications/unread-count/`

### Mark Notification as Read
- **Endpoint:** `POST /api/v1/notifications/{notif_id}/read/`

### Mark All Read
- **Endpoint:** `POST /api/v1/notifications/mark-all-read/`

---

## 10. Licensing & Rights

### List Track Clearance Records
- **Endpoint:** `GET /api/v1/licensing/rights/`

### Track Clearance Detail
- **Endpoint:** `GET /api/v1/licensing/rights/{track_id}/`

### Submit Legal / Rights Inquiry
- **Endpoint:** `POST /api/v1/licensing/inquiry/`
- **Request Body:**
  ```json
  {
    "claimant_name": "Label Representative",
    "organization": "YBNL / EMPIRE",
    "email": "rights@empire.com",
    "track_or_album": "Metaverse",
    "inquiry_type": "LICENSING_OFFER",
    "message": "Proposed licensing clearance terms..."
  }
  ```

---

## 11. Moderation

### Submit Content Safety Report
- **Endpoint:** `POST /api/v1/moderation/report/`
- **Request Body:** `{"target_type": "POST", "target_id": "post-01", "reason": "SPAM", "details": "..."}`

### Moderation Queue (Staff / Moderator)
- **Endpoint:** `GET /api/v1/moderation/reports/`

### Apply Moderation Action
- **Endpoint:** `POST /api/v1/moderation/action/`
- **Request Body:** `{"report_id": "rep-001", "action": "REMOVE_CONTENT", "notes": "..."}`
