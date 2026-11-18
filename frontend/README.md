# JUSTBADDO — FRONTEND SYSTEM (PHASE 1)

## Overview

JustBaddo is an independent digital fan and discography platform dedicated to Olamide Baddo. This directory contains the complete, responsive, and interactive frontend prototype built for Phase 1 of the product development lifecycle.

The frontend is built using clean, semantic HTML5, modern Tailwind CSS 4, vanilla JavaScript organized into modular architectures, Lucide icons, and Google Fonts. It is designed specifically to be easily ported into Django templates in Phase 2.

---

## 1. Technology Stack

- **Markup:** Semantic HTML5 with accessibility attributes (`aria-label`, visible focus states).
- **Styling:** Tailwind CSS 4 browser runtime engine + custom design system variables in `static/css/styles.css`.
- **Typography:** Google Fonts (`Plus Jakarta Sans` for clean body text, `Syne` for editorial display headlines).
- **Iconography:** Lucide Icons.
- **Scripting:** Modular Vanilla JavaScript (ES6+ classes, reactive event bus, local storage state persistence).
- **Audio Prototyping:** Web Audio API harmonic tone synthesizer (zero copyrighted MP3s distributed).

---

## 2. Quick Start / Running the Frontend

To view and interact with the platform, simply serve this `frontend/` directory using any local web server:

```bash
# Option A: Python Built-in HTTP Server
cd frontend
python -m http.server 8000

# Option B: Node.js (npx serve)
npx serve frontend

# Option C: Direct browser viewing
# Open frontend/index.html directly in Chrome, Firefox, Safari, or Edge.
```

Once running, navigate to `http://localhost:8000` in your web browser.

---

## 3. Directory Structure

```text
frontend/
├── index.html                      # Homepage (Hero, Featured Albums, Popular Classics, Arena Preview)
├── pages/
│   ├── music.html                  # Music Discovery & Complete Discography Catalogue
│   ├── album.html                  # Album Detail Page (?slug=ikigai-vol-1, etc.)
│   ├── track.html                  # Track Detail View (?id=ikigai-02, verified credits)
│   ├── search.html                 # Global Instant Search across songs, albums, and community
│   ├── playlists.html              # Curated Editorial Playlists & Custom User Playlists
│   ├── community.html              # Fan Discussions Feed, New Post Composer & Threaded Comments
│   ├── fan-arena.html              # Fan Arena: Live Polls, Song Battles, Trivia Quiz & Leaderboard
│   ├── stories.html                # Fan Stories, Concert Reflections & Reading Modal
│   ├── timeline.html               # Chronological Career Milestones (2010–2024)
│   ├── dashboard.html              # Member Dashboard (Saved Songs, Stats, Playlists)
│   ├── profile.html                # Member Public Profile (Badges, History, Following)
│   ├── notifications.html          # Notification Center (Poll alerts, replies, updates)
│   ├── settings.html               # Account Preferences, Player & Privacy Controls
│   ├── login.html                  # Authentication: Sign In
│   ├── register.html               # Authentication: Join Community
│   ├── forgot-password.html        # Password Recovery Request
│   ├── about.html                  # Platform Mission, History & Independent Status
│   ├── contact.html                # Inquiries & Licensing Outreach
│   ├── community-guidelines.html   # Rules of Engagement & Moderation
│   ├── privacy.html                # Privacy Policy Draft
│   ├── terms.html                  # Terms of Service Draft
│   └── 404.html                    # 404 Not Found Screen
├── components/                     # Modular HTML snippets ready for Django template inclusion
│   ├── nav.html                    # Global Top Navigation Header
│   ├── footer.html                 # Global Footer
│   └── player.html                 # Persistent Bottom Player, Expanded Modal, Queue & Playlist Modals
└── static/
    ├── css/
    │   └── styles.css              # Custom theme variables, scrollbars, sliders, keyframe animations
    └── js/
        ├── core/
        │   ├── app.js              # Global bootstrapper, navigation, mobile drawer, shortcuts
        │   ├── state.js            # Central reactive state store & event bus
        │   ├── storage.js          # Safe localStorage wrapper with memory fallback
        │   └── ui.js               # Toast alerts, modals, dropdowns, tab switching
        ├── data/
        │   ├── catalogue.js        # Verified discography (albums, tracks, durations, credits, status)
        │   ├── community-data.js   # Fictional fan personas, sample discussions, comments
        │   ├── arena-data.js       # Live community polls, song battles, verified trivia quizzes
        │   ├── stories-data.js     # Long-form concert reflections & essays
        │   └── timeline-data.js    # Verified chronological milestones (2010–2024)
        ├── music/
        │   ├── provider-interface.js # Abstract audio provider contract
        │   ├── mock-provider.js    # Web Audio API harmonic synthesizer for demo testing
        │   ├── player.js           # Persistent player controller, scrubbing, volume, shuffle, repeat
        │   ├── queue.js            # Queue drawer manager, reordering, item removal
        │   └── playlists.js        # Playlist CRUD and track assignment
        └── pages/
            ├── album-page.js       # Dynamic album page loader
            ├── dashboard-page.js   # Dashboard statistics and saved tracks manager
            ├── music-page.js       # Dynamic catalogue filtering and sorting
            ├── playlists-page.js   # Playlist inspector and track removal
            ├── search-page.js      # Global live search query engine
            ├── stories-page.js     # Story reader and essay submission
            ├── timeline-page.js    # Milestones filtering and rendering
            └── track-page.js       # Dynamic track view and credits
```

---

## 4. Music Player Architecture

The music player is designed with a strict provider-agnostic abstraction:

1. **`AudioProviderInterface` (`static/js/music/provider-interface.js`):**
   Defines the contract (`loadTrack`, `play`, `pause`, `seek`, `setVolume`, `getDuration`, `getCurrentTime`).
2. **`MockAudioProvider` (`static/js/music/mock-provider.js`):**
   Uses the browser's native **Web Audio API** to generate gentle harmonic pulses and clock updates. It simulates accurate scrubbing, playback duration, and pause states with **zero copyrighted sound recordings**, completely obeying licensing directives.
3. **`JustBaddoPlayer` (`static/js/music/player.js`):**
   Connects UI controls to the active provider, advances the queue, handles shuffle/repeat, and synchronizes with `JustBaddoState`.
4. **State Persistence Across Pages:**
   Player state (active track, progress, volume, queue) is persisted in `localStorage`. Navigating between different pages restores state immediately so the listener's session is never interrupted.

---

## 5. Reusable Components

The platform uses consistent, reusable component patterns across all 23 views:
- **Top Navigation Bar:** Brand mark, nav links, global search with `/` keyboard trigger, unread notifications badge, user dropdown, mobile slide-over drawer.
- **Persistent Player Bar:** Bottom 80px bar with track art, title, artist, playback controls, scrubber, volume slider, queue trigger, expanded player button.
- **Expanded Player Modal:** Full-bleed artwork view, large scrubber, technical status badge, add-to-playlist action.
- **Queue Drawer:** Fly-out sidebar displaying upcoming tracks with active playing wave indicator and one-click removal.
- **Add to Playlist Modal:** Selection modal allowing users to save songs to existing playlists or create a new playlist on the fly.
- **Toast Notification Engine:** Non-intrusive alert pills for actions (voting, liking, saving tracks, queue updates).

---

## 6. Django Backend Integration Handoff Notes

When transitioning to Phase 2 (Django integration):
1. **Templates:**
   - Move `frontend/components/nav.html` to `templates/includes/nav.html`.
   - Move `frontend/components/footer.html` to `templates/includes/footer.html`.
   - Move `frontend/components/player.html` to `templates/includes/player.html`.
   - Use `base.html` extending these includes, placing page-specific blocks in `content`.
2. **Static Files:**
   - Move `frontend/static/` to `static/` or app-specific `static/` folders.
   - Replace relative file links with `{% static 'css/styles.css' %}`, `{% static 'js/core/app.js' %}`, etc.
3. **Dynamic Data:**
   - Replace `JUSTBADDO_CATALOGUE` JSON objects with Django template loops: `{% for track in album.tracks.all %}`.
   - Replace demonstration authentication with Django `django.contrib.auth`.
   - Connect audio provider interface to authorised streaming service (Phase 5) or direct object storage CDN (Phase 7).
