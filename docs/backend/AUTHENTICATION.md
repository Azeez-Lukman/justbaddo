# JUSTBADDO — AUTHENTICATION & ACCESS CONTROL SPECIFICATION

## 1. Authentication Strategy

JustBaddo employs a dual authentication model tailored for both server-rendered Django templates and REST API clients:

1. **Session Authentication (Web / Templates)**: Secure HTTP cookies (`sessionid`, `csrftoken`) managing state across page navigation.
2. **REST Client Compatibility**: Standard HTTP Basic / Token headers supported by Django REST Framework for headless API access.

---

## 2. Authentication Workflows

### A. Registration Workflow (`POST /api/v1/accounts/register/`)
1. User provides `username`, `email`, `password`, `agree_terms`, and optional `fav_era`.
2. Input sanitization validates:
   - Username: Alphanumeric + underscores only, 3–30 characters, unique case-insensitive.
   - Email: Valid email format, unique across users.
   - Password: Minimum 8 characters, validated by Django's `MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`, and `UserAttributeSimilarityValidator`.
   - Terms: Mandatory boolean confirmation of JustBaddo community guidelines.
3. System provisions:
   - Core `User` model instance with PBKDF2-SHA256 password hash.
   - Initialized Fan Profile with default tier (`Day One Disciple`) and baseline fan points.
   - Standard account settings (queue autoplay, audio synth preview enabled).
4. Returns HTTP 201 Created with provisioned profile data.

### B. Login Workflow (`POST /api/v1/accounts/login/`)
1. Accepts `username_or_email` and `password`.
2. Resolves email to username if an `@` character is present.
3. Authenticates against Django's cryptographic credential store.
4. If successful:
   - Issues active session cookie via `django.contrib.auth.login()`.
   - Returns full member profile and settings.
5. If invalid: Returns HTTP 401 Unauthorized with code `INVALID_CREDENTIALS`.

### C. Logout Workflow (`POST /api/v1/accounts/logout/`)
1. Destroys active Django session and flushes session cookies.
2. Returns HTTP 200 OK.

### D. Password Recovery Workflow (`POST /api/v1/accounts/password-reset/`)
1. User submits verified registration email.
2. If account exists, dispatches secure one-time password reset link to console mailer (or production SMTP in Phase 8).
3. Always returns generic success response to prevent email enumeration attacks.

---

## 3. Permissions & Role Hierarchy

JustBaddo defines 4 discrete access levels:

| Tier | Role | Capabilities |
|---|---|---|
| **Level 0** | Anonymous Guest | Browse verified music catalogue, read track credits, preview mock Web Audio synth pulses, read published stories, view public discussions. |
| **Level 1** | Registered Member | Create and edit custom playlists, post community topics, comment on threads, vote in Fan Arena polls & song battles, submit fan stories for review. |
| **Level 2** | Verified Fan | Special prestige tier earned via trivia achievements; eligible for exclusive poll ties and arena tournaments. |
| **Level 3** | Moderator / Staff | Access `/api/v1/moderation/reports/`, resolve safety flags, approve submitted fan stories, issue user sanctions. |
| **Level 4** | Platform Admin | Full access to Django Admin (`/admin/`), rights clearance management, and server settings. |

---

## 4. Frontend State Synchronization

To maintain parity with Phase 1 frontend state:
- When a user logs in, the response payload matches the `CURRENT_USER` schema stored in `frontend/static/js/core/storage.js`.
- The frontend reactive bus emits `EVENT_USER_LOGIN`, updating nav avatars, dashboard links, and personalization badges across the UI.
