# JUSTBADDO MUSIC — TODO

This file tracks the development, catalogue archiving, frontend implementation, backend architecture, and licensing tasks for the JustBaddo platform.

Update the checklist as work progresses.

---

## 1. Project Preparation & Foundation

- [x] Confirm free-first music access model.
- [x] Confirm Nigeria and international target territories.
- [x] Confirm dual licensing approach.
- [x] Establish recommended technology stack (HTML5, Tailwind CSS 4, Vanilla JS).
- [x] Prepare project documentation.
- [x] Initialize Git repository.
- [x] Establish frontend directory structure (`frontend/pages/`, `frontend/components/`, `frontend/static/`).
- [x] Set up development environment.

---

## 2. Frontend Development (Phase 1 — Complete)

- [x] Establish design system & tokens (charcoal/near-black backgrounds, warm amber accents, Plus Jakarta Sans, Syne).
- [x] Develop persistent bottom music player (`jb-persistent-player`).
- [x] Develop expanded music player modal (`jb-expanded-player-modal`).
- [x] Develop playback queue drawer (`jb-queue-drawer`) with real-time removal & clear actions.
- [x] Develop playlist creation & track assignment modal (`jb-add-to-playlist-modal`).
- [x] Develop global top navigation header with desktop links, search shortcut `/`, notifications menu, and user menu.
- [x] Develop mobile slide-over navigation drawer (`jb-mobile-drawer`).
- [x] Implement Homepage (`index.html`) with Hero, Album Showcase, Essential Tracks, Arena preview, and Community highlights.
- [x] Implement Music Catalogue page (`pages/music.html`) with type filters (Albums, EPs, Singles) and sorting.
- [x] Implement Dynamic Album Detail page (`pages/album.html`) with full tracklist and verified release credits.
- [x] Implement Track Detail view (`pages/track.html`) with technical audio parameters (BPM, Key, Producer, Status).
- [x] Implement Global Search page (`pages/search.html`) with real-time multi-category querying (tracks, albums, posts).
- [x] Implement Playlists Hub (`pages/playlists.html`) with editorial collections and user custom playlist inspector.
- [x] Implement Community Feed (`pages/community.html`) with post creation modal, threaded replies, and like reactions.
- [x] Implement Fan Arena (`pages/fan-arena.html`) with live voting polls, song battles, trivia challenge runner, and leaderboard.
- [x] Implement Fan Stories (`pages/stories.html`) with editorial article cards, reading modal, and story submission form.
- [x] Implement Career Timeline (`pages/timeline.html`) with chronological verified milestones (2010–2024).
- [x] Implement Member Dashboard (`pages/dashboard.html`) with saved tracks management, stats, and playlist shortcuts.
- [x] Implement Member Profile (`pages/profile.html`) with public tabs (discussions, playlists, badges).
- [x] Implement Notification Center (`pages/notifications.html`) with mark-as-read interaction.
- [x] Implement Account & Preferences (`pages/settings.html`) with audio, privacy, and profile configuration.
- [x] Implement Authentication screens (`pages/login.html`, `pages/register.html`, `pages/forgot-password.html`).
- [x] Implement Supporting & Legal pages (`pages/about.html`, `pages/contact.html`, `pages/community-guidelines.html`, `pages/privacy.html`, `pages/terms.html`, `pages/404.html`).
- [x] Implement Web Audio API zero-copyright demonstration audio synthesizer (`static/js/music/mock-provider.js`).
- [x] Maintain persistent player state (track, progress, volume, queue) across page navigation via `localStorage`.

---

## 3. Music Catalogue Research & Data

- [x] Record studio albums (Rapsodi, YBNL, BGEL, Street OT, Eyan Mayweather, The Glory, Lagos Nawa, Carpe Diem, UY Scuti, Unruly).
- [x] Record EPs (Ikigai / 生き甲斐, Vol. 1).
- [x] Record singles and collaborations (Motigbana, Science Student, Kana, Poverty Die, Woske, Oil & Gas, Pawon, Omo Ologo).
- [x] Verify tracklists and positions.
- [x] Verify release dates and years.
- [x] Verify producers (ID Cabasa, Pheelz, Young Jonn, P.Priime, Eskeez, Semzi, BBM, Magicsticks).
- [x] Record verified sources for discography entries.
- [x] Tag playback statuses (`METADATA_ONLY`, `AUTHORISED_PROVIDER`, `JUSTBADDO_STREAMING`, `RESTRICTED`, `WITHDRAWN`).

---

## 4. Backend Development (Phase 2 — Complete)

- [x] Configure Django project with environment-driven settings (`config/settings.py`).
- [x] Establish modular monolith architecture across 11 applications (`core`, `accounts`, `music`, `playback`, `playlists`, `community`, `arena`, `stories`, `notifications`, `licensing`, `moderation`).
- [x] Configure Django REST Framework with standardized exception formatting, custom pagination, and throttling.
- [x] Implement service and repository abstraction layer for all domain logic.
- [x] Implement Accounts & Authentication workflows (`register`, `login`, `logout`, `profile`, `settings`, `password-reset`).
- [x] Implement Music Catalogue REST endpoints (`artist`, `albums`, `singles`, `tracks`, `search`, `timeline`).
- [x] Implement Provider-Independent Playback architecture (`check`, `session`, `log`, `history`).
- [x] Implement Playlists REST API (CRUD, add track, remove track).
- [x] Implement Community Discussions REST API (feed, category filter, posts, threaded replies, reactions).
- [x] Implement Fan Arena REST API (polls, voting, song battles, trivia challenge runner with scoring, leaderboard).
- [x] Implement Fan Stories REST API (list, detail reader, submissions, moderation publishing).
- [x] Implement Notifications REST API (list, unread count badge, mark read).
- [x] Implement Licensing & Rights clearance endpoints and rightsholder inquiry desk.
- [x] Implement Moderation reporting, review queue, and disciplinary actions.
- [x] Connect template rendering for existing frontend pages (`frontend_views.py`).
- [x] Author comprehensive backend test suite (46 automated tests passing with 0 errors).
- [x] Produce backend architecture, API, authentication, and security specifications.

---

## 5. Database Development (Phase 3 — Upcoming)

- [ ] Design final PostgreSQL relational schema (Albums, Tracks, Artists, Contributors, Playlists, Posts, Comments, Polls, Battles, Stories, Notifications, RightsRecords).
- [ ] Implement Django ORM Models and field constraints.
- [ ] Create and execute initial migrations.
- [ ] Develop database seed system with verified Olamide discography archive.
- [ ] Configure PostgreSQL production connection pooling and backup strategy.

---

## 6. Provider Investigation (Phase 5)

- [ ] Research SoundCloud commercial integration permissions.
- [ ] Investigate YouTube embedding requirements.
- [ ] Review other potential authorised providers.
- [ ] Compare territory coverage (Nigeria vs International).
- [ ] Compare playback restrictions.
- [ ] Document the selected initial provider.

---

## 7. Licensing Outreach (Phase 6)

- [ ] Identify artist management contacts.
- [ ] Identify relevant record labels (Coded Tunes, YBNL Nation, EMPIRE).
- [ ] Identify master rights holders.
- [ ] Identify composition rights holders & publishers.
- [ ] Prepare licensing introduction.
- [ ] Consult music-rights legal counsel.
- [ ] Establish royalty reporting procedures.
