# JUSTBADDO MUSIC — TECHNICAL RECOMMENDATIONS & DECISIONS

## 1. Overall Product Architecture

Build JustBaddo as a music discovery and fan experience platform with its own player interface and a provider-independent backend.

Do not make the platform dependent on one external streaming provider. Maintain a clean boundary between catalogue metadata (which JustBaddo completely owns and structures) and audio playback delivery.

---

## 2. Frontend Development & Design Decisions (Phase 1)

### Technology Stack Confirmed
- **HTML5:** Semantic elements (`<main>`, `<header>`, `<article>`, `<nav>`, `<footer>`) with explicit ARIA accessibility tags.
- **Tailwind CSS 4:** Modern CSS variables and theme tokens defined in `styles.css`. No legacy JavaScript config files required.
- **Modular Vanilla JavaScript:** Plain ES6+ classes and objects without heavy framework overhead (React/Vue/Angular omitted as instructed).
- **Lucide Icons:** Uniform SVG icons initialized via `lucide.createIcons()` on page load and dynamically refreshed when modals/components mount.
- **Google Fonts:** `Syne` for bold editorial display headings; `Plus Jakarta Sans` for clean, accessible interface copy.

### Design System & Visual Identity
- **Dark Editorial Surface:** Deep charcoal background (`#070809` and `#0e1014`) with elevated card surfaces (`#14171e`) and subtle borders (`#222836`).
- **Warm Accent Colors:** Amber (`#f59e0b`) and orange (`#ea580c`) accents invoking energy, warmth, and Lagos street culture.
- **Zero Excessive Gradients:** Avoided distracting glassmorphism, heavy neon glows, and bloated animations.

---

## 3. Audio Player & Playback Abstraction

### Key Decision: Zero-Copyright Development Synthesizer
In strict adherence to the licensing directives (`docs/MUSIC/JUSTBADDO_MUSIC_LICENSING.md`):
- Access to commercial recordings requires explicit legal permissions.
- To enable full interactive testing of progress bars, scrubbing, queue transitions, volume controls, play/pause states, and audio timers without distributing unauthorized MP3 files, JustBaddo employs the **Web Audio API** in `MockAudioProvider`.
- It generates gentle harmonic frequency pulses keyed to track BPM and musical key, accurately driving playback progress and queue advancement while remaining 100% legally compliant.

### Provider Interface Contract
The frontend audio engine adheres to `AudioProviderInterface`:
```javascript
class AudioProviderInterface {
  loadTrack(track) {}
  play() {}
  pause() {}
  seek(seconds) {}
  setVolume(volume) {}
  getCurrentTime() {}
  getDuration() {}
}
```
When an authorized provider (SoundCloud / HLS / licensed CDN) is integrated in Phase 5 or Phase 7, only a new provider class needs to be instantiated, without modifying any UI or player control logic.

### Session Persistence Across Page Navigation
The player state (`currentTrack`, `currentTime`, `volume`, `queue`, `isShuffle`, `repeatMode`) is continuously synchronized to `localStorage`. When a user navigates between albums, community discussions, or the timeline, the player state is restored instantly without interrupting the listening session.

---

## 4. Transition to Django Backend (Phase 2 Roadmap)

### Recommended Template Organization
Port the frontend into Django template directories:
```text
templates/
├── base.html                        # Global layout importing CSS, JS, and global includes
├── includes/
│   ├── nav.html                     # From frontend/components/nav.html
│   ├── footer.html                  # From frontend/components/footer.html
│   ├── player.html                  # From frontend/components/player.html
│   └── modals/
│       ├── queue_drawer.html
│       ├── expanded_player.html
│       └── add_to_playlist.html
├── music/
│   ├── catalogue.html               # From frontend/pages/music.html
│   ├── album_detail.html            # From frontend/pages/album.html
│   └── track_detail.html            # From frontend/pages/track.html
├── community/
│   ├── feed.html                    # From frontend/pages/community.html
│   └── post_detail.html
├── arena/
│   └── index.html                   # From frontend/pages/fan-arena.html
├── accounts/
│   ├── login.html                   # From frontend/pages/login.html
│   ├── register.html                # From frontend/pages/register.html
│   └── profile.html                 # From frontend/pages/profile.html
└── dashboard/
    └── index.html                   # From frontend/pages/dashboard.html
```

### Static Asset Path Strategy
Replace static relative links with Django template tags:
```html
<link rel="stylesheet" href="{% static 'css/styles.css' %}">
<script src="{% static 'js/core/app.js' %}"></script>
```

### API Endpoint Mapping
Expose lightweight Django REST Framework endpoints for dynamic interaction:
- `GET /api/music/albums/`
- `GET /api/music/tracks/<id>/`
- `GET /api/music/search/?q=<query>`
- `POST /api/playlists/`
- `POST /api/community/posts/`
- `POST /api/arena/vote/`

---

## 5. Licensing & Rights Recommendations

1. **Maintain Track-Level Rights Status:**
   Every track in the database must retain an explicit `playback_status` field:
   - `METADATA_ONLY`
   - `AUTHORISED_PROVIDER`
   - `JUSTBADDO_STREAMING`
   - `RESTRICTED`
   - `WITHDRAWN`
2. **Dual Outreach Approach:**
   Initiate communication with artist management and master/publishing rights holders simultaneously.
3. **Territorial Verification:**
   Ensure playback permissions explicitly define target territories (Nigeria vs International).

---

## 6. Backend Development Decisions (Phase 2)

### 1. Modular Monolith over Microservices
- We confirmed the **Modular Django Monolith** design across 11 dedicated applications. This eliminates network serialization latency, simplifies database transactions, and avoids DevOps orchestration overhead while preserving clean domain isolation.

### 2. Service / Repository Layer as Phase 3 Bridge
- In strict adherence to Phase 2 boundaries (no premature database migrations or raw database models before Phase 3), business logic is encapsulated in Domain Services (`MusicService`, `PlaybackService`, `ArenaService`, etc.).
- Services use in-memory demonstration repositories that match the exact data schema established in the frontend.
- When PostgreSQL models and migrations are introduced in Phase 3, only the internal repository queries inside the Services will be swapped to Django ORM QuerySets without affecting serializers, views, or client API contracts.

### 3. Unified Error and Response Envelope
- Configured a global exception handler in `core.exceptions.custom_exception_handler` and response helpers in `core.response.py`.
- All endpoints predictably return `{ "status": "success" | "error", "message": "...", "data": {...}, "errors": {...} }`, eliminating inconsistencies across client consumption.

### 4. Zero-Copyright Playback Enforcement at API Gateway
- The `playback` app strictly blocks unauthorized streaming.
- `PlaybackCheckView` inspects the track's rights status before any session token can be issued.
- If a track is `METADATA_ONLY` or `RESTRICTED`, the API responds with HTTP 403 Forbidden.

### 5. Multi-tiered Security Foundations
- Installed `django-cors-headers` and configured `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`.
- Configured DRF throttling tiers (anonymous: 120/min, authenticated: 600/min, authentication attempts: 5/min).
- Password validation uses Django's full validator suite with a minimum length of 8 characters.

---

## 7. Database Development Decisions & PostgreSQL Best Practices (Phase 3)

### 1. Relational Integrity via Database-Level Unique Constraints
- Rather than relying solely on application-layer checks, business integrity rules are strictly enforced at the PostgreSQL engine level:
  - **`unique_together = ('poll', 'user')`** prevents duplicate votes in Fan Arena polls.
  - **`unique_together = ('battle', 'user')`** guarantees single voting in song battles.
  - **`unique_together = ('post', 'user')`** prevents duplicate likes on community posts.
  - **`unique_together = ('playlist', 'track')`** and `('playlist', 'order')` ensure deterministic track ordering within playlists.
  - **`unique_together = ('follower', 'following')`** prevents duplicate follow records.

### 2. Normalized Discography Architecture
- Separate `Artist`, `Genre`, `Album`, and `Track` models eliminate metadata redundancy.
- Track metadata references album through explicit foreign keys (`CASCADE` on album deletion, `CASCADE` on track deletion).
- Rights records (`RightsRecord`) link 1:1 with tracks to maintain explicit compliance records for territory restrictions and authorized streaming links without modifying core music metadata.

### 3. Precomputed Transactional Denormalization
- High-read community endpoints (feed, post details, poll choices) benefit from denormalized counter fields (`likes_count`, `comments_count`, `votes`).
- When a user likes a post or votes in a poll, counters are updated transactionally alongside the creation of the relation record, eliminating costly `COUNT(*)` SQL aggregation queries under heavy read loads.

### 4. Idempotent Catalogue Seeding Architecture
- Created `music/management/commands/seed_catalogue.py` as an idempotent script utilizing `get_or_create()`.
- The seeder can be run safely during local setup, staging provisioning, and CI test pipelines (`JustBaddoTestCase` in `core/test_base.py`) without generating duplicated discography records or colliding primary keys.

### 5. Zero-Downtime Migration Policy
- Standardized migration rules: all new schema columns must provide explicit default values or specify `null=True`.
- Replaced direct in-place column renames with an expand-and-contract deployment strategy.
- Mandated `CONCURRENTLY` index creation for future large-table schema evolutions in production.

### 6. Verified Logical Backup and Disaster Recovery Strategy
- Confirmed custom PostgreSQL archive format (`pg_dump -Fc`) as the standard backup artifact, offering compression and fine-grained selective restore capabilities via `pg_restore`.
- Executed and validated a full backup and restore cycle on an isolated PostgreSQL test database (`justbaddo_db_restore_test`), confirming 100% record match and zero data loss.

---

## 8. Testing & Frontend-to-Backend Integration Decisions (Phase 4)

### 1. Unified API Client Singleton (`api-client.js`)
- Rather than scattering raw `fetch()` calls across 20+ vanilla JavaScript modules, centralized all HTTP communications into `window.JustBaddoApi`.
- **Automatic CSRF Token Extraction:** Parses `csrftoken` from `document.cookie` and injects `X-CSRFToken` header on all non-safe HTTP methods (`POST`, `PUT`, `PATCH`, `DELETE`).
- **Standardized Credentials:** Uses `credentials: 'include'` on every request to ensure Django session cookies (`sessionid`) are reliably passed across same-origin and configured CORS endpoints.
- **Envelope Unwrapping:** Standardizes unwrap of DRF's `{status, data, message, meta}` envelope while providing predictable error objects to callers.

### 2. Hybrid Graceful Degradation & Fallback Strategy
- To protect user experience during network outages, unseeded database environments, or local static inspections, frontend view controllers implement a graceful degradation pattern:
  - Controllers attempt live REST API fetch first.
  - If the server responds with an error or is unreachable, the UI falls back smoothly to local cached/demonstration records (`ALBUMS_DATA`, `TIMELINE_DATA`, `STORIES_DATA`).
  - This ensures that UI components never break or render blank states even during transitional development or server maintenance.

### 3. Audio Telemetry & Session Logging Strategy
- To maintain accurate listening counts and audit records without overloading the database:
  - Playback session initiation (`POST /api/v1/playback/session/`) checks track rights and issues a verified session record before the player activates audio synthesis.
  - Listening history telemetry is logged via `POST /api/v1/playback/log/` only when a track completes or reaches threshold listen time, updating `ListeningHistory` in PostgreSQL asynchronously without blocking the client playback loop.

### 4. Mutation Hardening & Anti-Spoofing Architecture
- During integration testing, security reviews revealed that several creation endpoints previously accepted client-supplied author usernames or permitted anonymous mutations.
- Hardened all write views (`PostListCreateView`, `PlaylistListCreateView`, `ModerationActionApplyView`, `CurrentUserProfileView`) to strictly verify `request.user.is_authenticated`.
- Author attribution is derived strictly from `request.user`, preventing impersonation and ensuring referential integrity in PostgreSQL.

### 5. PostgreSQL Constraint Propagation to Frontend Feedback
- Database-level unique constraints (e.g. `unique_together` on votes and likes) are mapped through DRF serializers to return clean HTTP 400 responses with descriptive messages (`"You have already voted in this poll"`).
- Frontend UI modules catch these constraint errors and display user-friendly toast messages, preventing unhandled promise rejections or ambiguous generic errors.
