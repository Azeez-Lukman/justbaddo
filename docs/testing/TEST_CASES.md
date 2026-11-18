# JUSTBADDO — TEST CASES SPECIFICATION

## 1. Overview & Test Matrix Summary

This document details the complete automated test suite for JustBaddo, encompassing **54 test cases** across 12 test suites. All tests execute against the PostgreSQL database engine using [`JustBaddoTestCase`](file:///c:/Users/USER/Documents/JustBaddo/core/test_base.py).

| Suite | File | Test Count | Pass Rate | Execution Time |
|---|---|---|---|---|
| **End-to-End Integration** | `core/tests_integration.py` | 7 | 100% (7/7) | ~14s |
| **Core & System Health** | `core/tests.py` | 2 | 100% (2/2) | ~4s |
| **Accounts & Auth** | `accounts/tests.py` | 5 | 100% (5/5) | ~12s |
| **Music Catalogue** | `music/tests.py` | 4 | 100% (4/4) | ~10s |
| **Playback & Telemetry** | `playback/tests.py` | 4 | 100% (4/4) | ~10s |
| **Phase 6 Playback Activation** | `playback/tests_phase6.py` | 8 | 100% (8/8) | ~9s |
| **Playlists** | `playlists/tests.py` | 4 | 100% (4/4) | ~9s |
| **Community Feed & Posts** | `community/tests.py` | 6 | 100% (6/6) | ~14s |
| **Fan Arena** | `arena/tests.py` | 7 | 100% (7/7) | ~18s |
| **Fan Stories** | `stories/tests.py` | 4 | 100% (4/4) | ~9s |
| **Notifications** | `notifications/tests.py` | 6 | 100% (6/6) | ~15s |
| **Licensing & Rights** | `licensing/tests.py` | 4 | 100% (4/4) | ~10s |
| **Moderation** | `moderation/tests.py` | 4 | 100% (4/4) | ~9s |
| **TOTAL** | **13 Test Suites** | **62 Tests** | **100% PASS** | **124.12s** |

---

## 2. Detailed Test Cases

### Suite 1: End-to-End Integration (`core/tests_integration.py`)

#### TC-INT-001: Frontend Template Rendering & Static Asset Mapping
- **Target**: `GET /`, `GET /index.html`, `GET /pages/<page_name>.html` (22 pages)
- **Input**: Anonymous HTTP GET requests across root and all subpages.
- **Expected Outcome**: HTTP 200 OK across all 23 views; template contains branding elements ("JUSTBADDO"), CSS link (`styles.css`), and JavaScript client (`api-client.js`).
- **Result**: PASS

#### TC-INT-002: Complete Authentication Journey
- **Target**: `/api/v1/accounts/register/`, `/api/v1/accounts/login/`, `/api/v1/accounts/profile/`, `/api/v1/accounts/settings/`, `/api/v1/accounts/logout/`
- **Workflow**:
  1. Register user `integrator_baddo` with terms acceptance.
  2. Attempt duplicate registration (assert HTTP 400 Bad Request).
  3. Authenticate with credentials and establish session.
  4. Fetch current user profile from PostgreSQL (assert username match).
  5. Update account settings via PUT (assert persistence).
  6. Logout and verify `/api/v1/accounts/profile/` returns HTTP 401/403.
- **Result**: PASS

#### TC-INT-003: Music Catalogue to Playback Telemetry Flow
- **Target**: `/api/v1/music/albums/`, `/api/v1/music/albums/rapsodi/`, `/api/v1/music/tracks/<id>/`, `/api/v1/licensing/check/<id>/`, `/api/v1/playback/session/`, `/api/v1/playback/log/`, `/api/v1/playback/history/`
- **Workflow**:
  1. Retrieve verified albums list (verify $\ge 5$ albums).
  2. Inspect *Rapsodi* detail and track list.
  3. Validate licensing rights for track `rap-01`.
  4. Initialize playback session.
  5. Log completed playback of 180 seconds.
  6. Retrieve listening history and assert track appears in PostgreSQL `ListeningHistory`.
- **Result**: PASS

#### TC-INT-004: Community Post, Comment, and Unique Like Constraint
- **Target**: `/api/v1/community/posts/`, `/api/v1/community/posts/<id>/comments/`, `/api/v1/community/posts/<id>/like/`
- **Workflow**:
  1. Authenticated user creates post in category "Discussion".
  2. Adds threaded comment to the newly created post.
  3. Toggles like ON (assert `has_liked = True`, `likes = 1`).
  4. Toggles like OFF (assert `has_liked = False`, `likes = 0`).
  5. Verifies PostgreSQL unique constraint prevents duplicate like rows.
- **Result**: PASS

#### TC-INT-005: Fan Arena Poll and Battle Voting Integration
- **Target**: `/api/v1/arena/polls/`, `/api/v1/arena/polls/<id>/vote/`, `/api/v1/arena/battles/<id>/vote/`
- **Workflow**:
  1. Query active community polls.
  2. Cast vote on option A (assert HTTP 200 OK).
  3. Cast second vote on same poll by same user (assert HTTP 400 Bad Request).
- **Result**: PASS

#### TC-INT-006: Playlist Lifecycle Integration
- **Target**: `/api/v1/playlists/`, `/api/v1/playlists/<id>/tracks/`, `/api/v1/playlists/<id>/`
- **Workflow**:
  1. Create custom playlist "Night Drives in Bariga".
  2. Add track to playlist using string `track_id`.
  3. Remove track from playlist.
  4. Delete playlist.
- **Result**: PASS

#### TC-INT-007: Unauthenticated Protected Route Rejection
- **Target**: `/api/v1/playlists/` (POST), `/api/v1/community/posts/` (POST), `/api/v1/moderation/action/` (POST)
- **Workflow**:
  1. Logout user.
  2. Attempt to create playlist (assert HTTP 401/403).
  3. Attempt to create community post (assert HTTP 401/403).
  4. Attempt to execute moderation action (assert HTTP 401/403).
- **Result**: PASS

---

### Suite 2: Core & System Health (`core/tests.py`)

- **TC-COR-001**: System Health Check (`GET /api/v1/health/`) — Verifies HTTP 200 and healthy service status.
- **TC-COR-002**: Platform Metadata (`GET /api/v1/platform/`) — Verifies artist name, platform branding, and legal affiliation disclaimer.

---

### Suite 3: Accounts & Authentication (`accounts/tests.py`)

- **TC-ACC-001**: User Registration Success — Creates new user with valid username, email, password, and terms agreement.
- **TC-ACC-002**: User Registration Missing Terms — Verifies rejection with HTTP 400 when `agree_terms = False`.
- **TC-ACC-003**: User Authentication — Verifies login with valid credentials returns session cookie and user profile.
- **TC-ACC-004**: Authenticated Profile Fetch — Verifies authenticated user receives their own profile attributes.
- **TC-ACC-005**: Unauthenticated Profile Access — Verifies anonymous request to `/api/v1/accounts/profile/` returns HTTP 401/403.

---

### Suite 4: Music Discovery & Discography (`music/tests.py`)

- **TC-MUS-001**: Artist Profile — Verifies Olamide artist record, verification status, and genres.
- **TC-MUS-002**: Album Catalogue Listing — Verifies verified studio albums (Rapsodi, YBNL, BGEL, Street OT, Carpe Diem).
- **TC-MUS-003**: Album Detail & Tracklist — Verifies track metadata, track numbers, and audio BPM/key attributes.
- **TC-MUS-004**: Music Search — Queries "Eni Duro" and confirms matching track records returned.

---

### Suite 5: Playback & Telemetry (`playback/tests.py`)

- **TC-PBK-001**: Availability Check Playable — Verifies authorized track returns `can_play = True`.
- **TC-PBK-002**: Availability Check Restricted — Verifies restricted track returns `can_play = False`.
- **TC-PBK-003**: Playback Session Creation — Verifies session initialization token.
- **TC-PBK-004**: Listening History Telemetry — Verifies play event logging into PostgreSQL.

---

### Suite 6: Playlists Management (`playlists/tests.py`)

- **TC-PLS-001**: List Playlists — Retrieves user and curated playlists.
- **TC-PLS-002**: Create and Delete Playlist — Validates playlist creation and deletion by owner.
- **TC-PLS-003**: Add Track to Playlist — Verifies through-model ordering and association.
- **TC-PLS-004**: Playlist Detail Retrieval — Inspects full tracklist within a playlist.

---

### Suite 7: Community & Social Engagement (`community/tests.py`)

- **TC-COM-001**: List Community Posts — Retrieves paginated feed of fan discussions.
- **TC-COM-002**: Filter Posts by Category — Filters posts by category tag.
- **TC-COM-003**: Create Community Post — Authenticated creation of fan discussion thread.
- **TC-COM-004**: Threaded Comment Submission — Adds comment to existing post.
- **TC-COM-005**: Toggle Like Reaction — Verifies like counter increment and decrement.
- **TC-COM-006**: Follow User — Toggles following relationship on user profile.

---

### Suite 8: Fan Arena (`arena/tests.py`)

- **TC-ARN-001**: List Live Polls — Verifies poll options and vote percentages.
- **TC-ARN-002**: Cast Poll Vote — Records authenticated vote and recalculates percentage bars.
- **TC-ARN-003**: List Song Battles — Retrieves head-to-head song battles.
- **TC-ARN-004**: Cast Song Battle Vote — Records vote for song A or song B.
- **TC-ARN-005**: Retrieve Trivia Challenge — Fetches 5 trivia questions with options.
- **TC-ARN-006**: Submit Trivia Answer Sheet — Validates answer scoring and feedback.
- **TC-ARN-007**: Leaderboard Retrieval — Verifies leaderboard rankings and points.

---

### Suite 9: Fan Stories (`stories/tests.py`)

- **TC-STO-001**: List Approved Stories — Retrieves published fan essays.
- **TC-STO-002**: Story Reader Detail — Retrieves full story text and cover artwork.
- **TC-STO-003**: Submit Fan Story — Submits new essay into moderation queue (`PENDING`).
- **TC-STO-004**: Story Moderation Status Filter — Verifies unapproved stories remain hidden from public feed.

---

### Suite 10: In-App Notifications (`notifications/tests.py`)

- **TC-NOT-001**: List Notifications — Retrieves user notifications.
- **TC-NOT-002**: Unread Count Badge — Retrieves numerical count of unread items.
- **TC-NOT-003**: Mark Notification Read — Updates `is_read = True` for single item.
- **TC-NOT-004**: Mark All Read — Updates all notifications for user.
- **TC-NOT-005**: Notification Timestamp Ordering — Verifies newest-first ordering.
- **TC-NOT-006**: Notification Isolation — Verifies users only see their own notifications.

---

### Suite 11: Licensing & Rights Clearance (`licensing/tests.py`)

- **TC-LIC-001**: List Rights Records — Retrieves verified rights records.
- **TC-LIC-002**: Track Clearance Check — Checks clearance status and authorized platforms.
- **TC-LIC-003**: Rights Inquiry Submission — Submits rightsholder licensing inquiry.
- **TC-LIC-004**: Zero-Copyright Compliance — Confirms no binary audio is served via API.

---

### Suite 12: Moderation & Safety (`moderation/tests.py`)

- **TC-MOD-001**: Submit Content Report — Flags post/comment for review.
- **TC-MOD-002**: List Moderation Queue — Staff review of pending reports.
- **TC-MOD-003**: Execute Moderation Action — Applies disciplinary resolution.
- **TC-MOD-004**: User Restriction Enforcement — Verifies user restrictions table.

---

### Suite 13: Phase 6 Playback & Provider Activation (`playback/tests_phase6.py`)

- **TC-P6-001: Availability States Verification**
  - **Target**: `GET /api/v1/playback/check/<track_id>/`
  - **Scenario**: Validates classification across all 5 availability states (`metadata_only`, `provider_available`, `self_hosted_available`, `restricted`, `withdrawn`). Confirms that only cleared states allow `can_play = True`.
  - **Result**: PASS

- **TC-P6-002: Territory Restriction Enforcement**
  - **Target**: `GET /api/v1/playback/check/<track_id>/?territory=...` & `POST /api/v1/playback/session/`
  - **Scenario**: Tests track restricted to Nigeria & Ghana (`['NG', 'GH']`). Verifies territory `NG` succeeds, while territory `US` receives `can_play = False` and HTTP 403 Forbidden on session initialization.
  - **Result**: PASS

- **TC-P6-003: Expired Licensing Permissions Blocker**
  - **Target**: `POST /api/v1/playback/session/`
  - **Scenario**: Tests track with `valid_until` in the past. Verifies `rights_status = 'expired'` and session creation is strictly rejected with HTTP 403.
  - **Result**: PASS

- **TC-P6-004: Future Effective Start Date Blocker**
  - **Target**: `GET /api/v1/playback/check/<track_id>/`
  - **Scenario**: Tests track with `valid_from` set in the future. Verifies `rights_status = 'pending_start'` and `can_play = False`.
  - **Result**: PASS

- **TC-P6-005: Playback Session Provider Capabilities Profile**
  - **Target**: `POST /api/v1/playback/session/`
  - **Scenario**: Verifies that session creation returns supported provider capability profile (`can_seek`, `can_change_volume`, `supports_headless`, `requires_user_gesture`).
  - **Result**: PASS

- **TC-P6-006: Duplicate Completion Event Telemetry Deduplication**
  - **Target**: `POST /api/v1/playback/log/`
  - **Scenario**: Submits two identical completion events within 60 seconds. Verifies the second event returns `status: 'duplicate_suppressed'` without creating duplicate rows in `ListeningHistory`.
  - **Result**: PASS

- **TC-P6-007: Session Invalidation Post-Completion**
  - **Target**: `POST /api/v1/playback/log/`
  - **Scenario**: Verifies that upon completion log, `session.is_valid` is set to `False` and `ended_at` is populated. Further log attempts with the same session token are rejected.
  - **Result**: PASS

- **TC-P6-008: User Listening History Privacy Preference Guard**
  - **Target**: `GET /api/v1/playback/history/?username=<username>`
  - **Scenario**: Verifies that when a user sets `private_listening_activity = True` in Account Settings, third-party viewers receive an empty list (`[]`), while the user themselves retains full access to their history.
  - **Result**: PASS
