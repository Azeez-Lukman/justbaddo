# JUSTBADDO — BACKEND SECURITY ARCHITECTURE

## 1. Security Philosophy & Principles

As an independent, community-driven platform, JustBaddo's security architecture focuses on:
1. Protecting fan data and account privacy.
2. Preventing content abuse and malicious injections.
3. Strictly safeguarding copyrighted audio recordings and intellectual property boundaries.
4. Defending server infrastructure against DDoS, credential stuffing, and bot scraping.

---

## 2. Threat Mitigations & Controls

### A. Authentication & Password Security
- Passwords are never stored in plaintext. They are salted and hashed using standard PBKDF2 with SHA-256 (Django default).
- Strict password complexity enforcement via `MinimumLengthValidator` (min 8 chars), `CommonPasswordValidator`, `NumericPasswordValidator`, and `UserAttributeSimilarityValidator`.
- Brute-force protection: Authentication endpoints (`/api/v1/accounts/login/`, `/api/v1/accounts/register/`) are throttled to a maximum of 5 attempts per minute per IP address.

### B. CSRF Protection
- All mutating endpoints (`POST`, `PUT`, `PATCH`, `DELETE`) require a valid `X-CSRFToken` header or cookie validation.
- Configured with `CSRF_COOKIE_HTTPONLY = False` allowing the frontend client to extract the token safely from JavaScript for asynchronous `fetch()` requests.
- `CSRF_TRUSTED_ORIGINS` explicitly restricts allowed origins to designated development and production domains.

### C. Rate Limiting & Throttling
Configured centrally in `REST_FRAMEWORK` settings:
- **Anonymous Visitors:** `120 requests / minute` (prevents scraping catalogue and spamming poll counters).
- **Authenticated Users:** `600 requests / minute` (ample headroom for interactive community discussions and music browsing).
- **Authentication Routes:** `5 requests / minute` (mitigates dictionary attacks and brute-force registration scripts).

### D. Media & File Upload Safeguards
- File uploads (such as avatars or story hero attachments) are strictly limited:
  - `MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024` (5 MB maximum).
  - Whitelist of allowed image extensions: `.jpg`, `.jpeg`, `.png`, `.webp`.
  - Executable scripts (`.exe`, `.sh`, `.php`, `.py`, `.html`) are permanently disallowed.

### E. Audio & Intellectual Property Protection
- The backend contains **no endpoints for uploading, downloading, or streaming copyrighted MP3 or WAV master recordings**.
- The `playback` application checks rights availability per track. Unclear or restricted tracks return HTTP 403 Forbidden.
- Playback for development uses client-side Web Audio API synthetic previews, ensuring full compliance with international copyright treaties and Nigerian copyright statutes.

### F. Environment Variable Isolation
- Sensitive credentials (`DJANGO_SECRET_KEY`, `POSTGRES_PASSWORD`, `DATABASE_URL`) are read strictly from operating system environment variables.
- Default fallback keys are restricted to development mode and accompanied by warnings.
- No production secrets are committed to Git.
