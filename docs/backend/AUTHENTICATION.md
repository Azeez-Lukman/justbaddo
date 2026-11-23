# JUSTBADDO — AUTHENTICATION EXPERIENCE & SESSION MANAGEMENT ARCHITECTURE

## 1. Product Decisions & Architectural Overview

The authentication and session management layer for JustBaddo adheres to four core product decisions:

- **Authentication Presentation:** `dedicated` — Full dedicated authentication pages (`/pages/login.html`, `/pages/register.html`, `/pages/forgot-password.html`, `/pages/reset-password.html`, `/pages/verify-email.html`, `/pages/welcome.html`). No cluttered pop-ups or third-party modal dependencies for primary credentials.
- **Account Navigation:** `avatar` — Authenticated state renders the member's profile avatar with an automatic monogram initials fallback (`getInitials`) if the avatar is missing or fails to load. The account dropdown menu exposes member-only shortcuts (`My profile`, `Saved music`, `My playlists`, `Community`, `Account settings`, `Sign out`). Guests are never exposed to member controls and see clean "Sign In" and "Join JustBaddo" actions.
- **Post-Sign-In Destination:** `context` — Preserves the intended visitor destination via a safe `next` parameter (e.g. saving a track, creating a playlist, replying to a discussion, voting in a poll). Validated server-side using Django's `url_has_allowed_host_and_scheme` to completely eliminate open redirect vulnerabilities.
- **Sign-Out Behaviour:** `instant` — Immediate POST request to `/api/v1/accounts/logout/` with CSRF defense. Destroys the Django session via `request.session.flush()`, purges client-side private state and local storage caches, returns the member to the public homepage (`/`), and displays a non-intrusive confirmation toast: *"You've been signed out."* Stale page inspection via browser history back-navigation is blocked via `Cache-Control: no-cache, no-store, must-revalidate`.

---

## 2. Dedicated Authentication Pages

| Page Route | Purpose | Key Capabilities |
|---|---|---|
| `/pages/login.html` | Member sign-in | Accepts username or email; password visibility toggle; forgotten password link; inline field validation; loading spinner during submission; retention of non-sensitive inputs on error; account-enumeration defense; context destination preservation (`?next=`). |
| `/pages/register.html` | Fan registration | Collects Username, Display Name, Email, Password, Terms/Privacy acceptance; strong password validation; duplicate username/email detection; loading state; redirects to welcome state while preserving context. |
| `/pages/forgot-password.html` | Password recovery | Email entry; generic uniform success banner to prevent user account enumeration; preserves return destination. |
| `/pages/reset-password.html` | New password selection | Token and UID validation via URL query parameters (`?uid=...&token=...`); strong password validation and confirmation; links to sign in upon success. |
| `/pages/verify-email.html` | Account verification | Verifies account cryptographic token via `/api/v1/accounts/verify-email/`; visual state indicators for pending, success, and expired tokens. |
| `/pages/welcome.html` | Member onboarding | Registration success welcome state; personalized greeting; direct links to discography and arena; context continuation card if visitor had an action pending. |

---

## 3. Endpoints & API Routing (`/api/v1/accounts/`)

| Method | Endpoint | Description | Permissions | Throttling |
|---|---|---|---|---|
| `POST` | `/api/v1/accounts/login/` | Authenticate user via username or email; cycle session key; configure `remember_me` session expiry (2 weeks vs session); safely validate `next` destination. | `AllowAny` | `auth_attempt` (5/min) |
| `POST` | `/api/v1/accounts/register/` | Register new user; create `UserProfile` and `AccountSettings`; issue email verification token. | `AllowAny` | `auth_attempt` (5/min) |
| `POST` | `/api/v1/accounts/logout/` | Instant logout; flush session; issue `Cache-Control: no-cache, no-store, must-revalidate, max-age=0`. | `AllowAny` | None |
| `POST` | `/api/v1/accounts/password-reset/` | Request password reset instructions; non-enumerating generic response. | `AllowAny` | `auth_attempt` (5/min) |
| `POST` | `/api/v1/accounts/password-reset/confirm/` | Reset password using base64 `uid`, cryptographic `token`, and `new_password`. | `AllowAny` | `auth_attempt` (5/min) |
| `POST` / `GET` | `/api/v1/accounts/verify-email/` | Verify user email using base64 `uid` and `token`. | `AllowAny` | None |
| `GET` / `PATCH` | `/api/v1/accounts/profile/` | Inspect and edit authenticated member profile. | `IsAuthenticated` | Default user rate |
| `GET` | `/api/v1/accounts/users/<username>/` | Retrieve public fan profile. | `AllowAny` | Default anon rate |
| `GET` / `PATCH` | `/api/v1/accounts/settings/` | Retrieve and update account preferences. | `AllowAny` (Authenticated or fallback) | Default user rate |

---

## 4. Session & Security Configuration

The Django configuration adheres to strict security defaults across local and production environments:

- **HTTP-Only Cookies:** `SESSION_COOKIE_HTTPONLY = True` prevents client JavaScript access to session identifiers, guarding against XSS session hijacking.
- **SameSite Protection:** `SESSION_COOKIE_SAMESITE = 'Lax'` and `CSRF_COOKIE_SAMESITE = 'Lax'` mitigate cross-site request forgery attacks.
- **HTTPS Enforcement:** `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` enabled in `config/settings_production.py`.
- **Session Duration:** `SESSION_COOKIE_AGE = 1209600` (2 weeks). When `remember_me` is unchecked, `request.session.set_expiry(0)` causes the session cookie to expire when the user closes their browser.
- **Session Fixation Defense:** Calling Django's `login(request, user)` automatically invokes `request.session.cycle_key()`, issuing a fresh session key post-authentication.
- **Rate Limiting:** Authentication attempt endpoints (`login/`, `register/`, `password-reset/`, `password-reset/confirm/`) are constrained to `5/min` via `ScopedRateThrottle`.

---

## 5. Context Preservation & Safe Redirection

Whenever an unauthenticated visitor attempts an interactive, member-only action (such as saving a track to their library, adding a song to a playlist, starting a community discussion, or voting in a song battle):

1. The frontend invokes `JustBaddoUI.requireAuth(actionDescription)`.
2. A warning toast informs the guest: *"Please sign in to <action>."*
3. The guest is smoothly routed to `/pages/login.html?next=<encodedCurrentPath>`.
4. Upon successful credentials verification, `LoginView` validates the target URL using `AccountService.validate_safe_redirect`:
   ```python
   url_has_allowed_host_and_scheme(
       url=redirect_url,
       allowed_hosts={request.get_host()},
       require_https=request.is_secure()
   )
   ```
5. Untrusted or external URLs (e.g., `https://attacker.com`) are stripped and replaced with the safe default (`/pages/dashboard.html` or `/`).

---

## 6. Test Suite & Verification Matrix

The authentication test suite in `accounts/tests.py` covers 20 unit and integration tests executing against PostgreSQL 18:

| Test Case | Method | Purpose |
|---|---|---|
| `test_register_user_success` | POST | Valid registration creates User, UserProfile, AccountSettings, and verification token. |
| `test_register_missing_terms_fails` | POST | Fails with HTTP 400 when Terms & Privacy acceptance is omitted. |
| `test_register_duplicate_username_fails` | POST | Rejects duplicate username with field error. |
| `test_register_duplicate_email_fails` | POST | Rejects existing email address with field error. |
| `test_register_weak_password_fails` | POST | Enforces minimum length and validator rules. |
| `test_login_demo_user` | POST | Authenticates username, returns profile and redirect destination. |
| `test_login_with_email` | POST | Authenticates using email address interchangeably. |
| `test_login_invalid_password_rejected` | POST | Returns HTTP 401 with generic `INVALID_CREDENTIALS` code. |
| `test_login_nonexistent_user_rejected` | POST | Returns HTTP 401 without user enumeration. |
| `test_rate_limiting_enforced_after_repeated_attempts` | POST | Confirms `auth_attempt` throttle triggers HTTP 429 after 5 failed attempts. |
| `test_login_safe_redirect_preservation` | POST | Preserves internal redirect target (`/pages/community.html?post=post-1`). |
| `test_login_rejects_open_redirect` | POST | Sanitizes phishing URLs (`https://evil-phishing-site.com`) to `/pages/dashboard.html`. |
| `test_logout_post_invalidates_session` | POST | Confirms session destruction, `Cache-Control: no-cache`, and profile protection. |
| `test_password_reset_request_nonexistent_email_no_enumeration` | POST | Returns uniform HTTP 200 generic success message. |
| `test_password_reset_and_confirm_flow` | POST | Validates end-to-end token generation, password change, and re-authentication. |
| `test_email_verification_flow` | POST | Verifies user email via cryptographic token, setting `is_verified=True`. |
| `test_get_profile` | GET | Authenticated profile retrieval. |
| `test_get_profile_unauthenticated` | GET | Unauthorized access yields HTTP 401/403. |
| `test_get_public_profile` | GET | Open visitor access to public profile. |
| `test_get_and_update_settings` | GET/PATCH | Preference retrieval and update. |

**Full Project Test Suite Result:** Ran 75 tests across all 11 Django apps against PostgreSQL 18 — 100% Passing (0 failures, 0 errors).
