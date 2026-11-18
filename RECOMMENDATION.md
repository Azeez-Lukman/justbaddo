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
