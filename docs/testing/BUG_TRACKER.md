# JUSTBADDO — BUG TRACKER & DEFECT RESOLUTION LOG

## 1. Overview & Issue Lifecycle

This document logs all functional, structural, and security defects identified during **Phase 4: Testing and Integration**. Every issue includes detailed reproduction steps, root cause analysis, corrective actions taken, and verification status against automated test suites.

| Defect ID | Severity | Module | Description | Resolution Status |
|---|---|---|---|---|
| **BUG-001** | High | `core` / Routing | Missing `/index.html` URL Route (404 on home links from subpages) | **VERIFIED FIXED** |
| **BUG-002** | High | `community` | Incompatible category choices in `PostCreateSerializer` | **VERIFIED FIXED** |
| **BUG-003** | Critical | `arena` | Unenforced one-vote-per-user constraint due to missing user context | **VERIFIED FIXED** |
| **BUG-004** | Medium | `licensing` | Route mismatch between `/rights/<id>/` and `/check/<id>/` | **VERIFIED FIXED** |
| **BUG-005** | Medium | `playlists` | Integer primary key rejected by `add_track_to_playlist` | **VERIFIED FIXED** |
| **BUG-006** | Critical | `accounts` | Insecure demo user fallback allowing unauthorized profile access | **VERIFIED FIXED** |
| **BUG-007** | Medium | `accounts` | Missing `PUT` method on `AccountSettingsView` causing HTTP 405 | **VERIFIED FIXED** |
| **BUG-008** | Medium | `playback` | Playback telemetry log serializer parameter naming mismatch | **VERIFIED FIXED** |
| **BUG-009** | High | `frontend` | Frontend pages relying solely on mock scripts without API client | **VERIFIED FIXED** |
| **BUG-010** | High | `playback` | Serializer default boolean overwrite masking `completed: True` | **VERIFIED FIXED** |
| **BUG-011** | High | `playback` | Privacy attribute mismatch (`history_visibility` vs `private_listening_activity`) | **VERIFIED FIXED** |
| **BUG-012** | Low | `core` | Hardcoded active phase string expectation in metadata test | **VERIFIED FIXED** |

---

## 2. Detailed Bug Reports

### BUG-001: Missing `/index.html` Route
- **Severity**: High (Application Navigation Broken)
- **Module**: `config/urls.py`
- **Symptom**: Clicking "Home" or "Back to Home" from any subpage (`../index.html`) returned HTTP 404 Not Found when served via Django.
- **Root Cause**: `config/urls.py` mounted `IndexView` at `path('', ...)` but omitted `path('index.html', ...)`.
- **Resolution**: Added `path('index.html', IndexView.as_view(), name='frontend-index-html')`.
- **Verification**: `test_frontend_template_rendering_and_assets` verified HTTP 200 on `/index.html`.

---

### BUG-002: Incompatible Category Choices in `PostCreateSerializer`
- **Severity**: High (User Experience Broken)
- **Module**: `community/serializers.py`
- **Symptom**: Submitting discussion modal form in `community.html` produced HTTP 400 Bad Request error.
- **Root Cause**: The frontend select dropdown provided options `'Discussion'`, `'Album Analysis'`, and `'Catalogue Nostalgia'`, whereas the backend serializer strictly restricted choices to `['Discography', 'Lyrics & Meaning', 'Concerts & OLIC', 'General Fan Chat']`.
- **Resolution**: Expanded `PostCreateSerializer` choices in [`community/serializers.py`](file:///c:/Users/USER/Documents/JustBaddo/community/serializers.py) to include all frontend categories.
- **Verification**: `test_community_post_comment_and_unique_like_constraint` verified successful post creation with category `'Discussion'`.

---

### BUG-003: Unenforced One-Vote-Per-User Constraint in Fan Arena
- **Severity**: Critical (Data Integrity Violation)
- **Module**: `arena/views.py`
- **Symptom**: Authenticated users were able to cast unlimited votes on polls and song battles.
- **Root Cause**: `PollVoteView.post` and `SongBattleVoteView.post` called domain services without passing `user=request.user`. In the service, `user` evaluated to `None`, bypassing the duplicate vote check.
- **Resolution**: Updated `PollVoteView` and `SongBattleVoteView` in [`arena/views.py`](file:///c:/Users/USER/Documents/JustBaddo/arena/views.py) to supply `user=request.user if request.user.is_authenticated else None`.
- **Verification**: `test_arena_poll_and_battle_voting_integration` confirmed that duplicate votes return HTTP 400 Bad Request.

---

### BUG-004: Route Mismatch for Track Rights Checking
- **Severity**: Medium (API Contract Inconsistency)
- **Module**: `licensing/urls.py`
- **Symptom**: `GET /api/v1/licensing/check/<track_id>/` returned HTTP 404 Not Found.
- **Root Cause**: `licensing/urls.py` only mounted `rights/<str:track_id>/`, while the frontend client requested `check/<str:track_id>/`.
- **Resolution**: Added alias `path('check/<str:track_id>/', RightsRecordDetailView.as_view(), name='rights-check')` in [`licensing/urls.py`](file:///c:/Users/USER/Documents/JustBaddo/licensing/urls.py).
- **Verification**: Verified via `test_music_catalogue_and_playback_telemetry_flow`.

---

### BUG-005: Type Inflexibility in `add_track_to_playlist`
- **Severity**: Medium (Data Validation Failure)
- **Module**: `playlists/services.py`
- **Symptom**: Adding tracks using integer IDs caused 400 Bad Request ("Track not found in catalogue").
- **Root Cause**: `PlaylistService.add_track_to_playlist` queried only `track_id__iexact=str(track_id)`. When integer database primary keys were supplied, the lookup returned `None`.
- **Resolution**: Updated [`playlists/services.py`](file:///c:/Users/USER/Documents/JustBaddo/playlists/services.py) to fall back to integer `id` lookup if string `track_id` lookup does not match.
- **Verification**: `test_playlist_lifecycle_integration` verified track addition and removal.

---

### BUG-006: Insecure Demo User Fallback in `CurrentUserProfileView`
- **Severity**: Critical (Security & Authorization Vulnerability)
- **Module**: `accounts/views.py`
- **Symptom**: Any anonymous visitor requesting `/api/v1/accounts/profile/` was automatically treated as logged in as `baddofan99`.
- **Root Cause**: `CurrentUserProfileView` declared `permission_classes = [AllowAny]` and defaulted `username = request.user.username if request.user.is_authenticated else 'baddofan99'`.
- **Resolution**: Changed permission class to `[IsAuthenticated]`. Anonymous requests return HTTP 401/403.
- **Verification**: `test_complete_authentication_journey` and `test_get_profile_unauthenticated` verified HTTP 401/403.

---

### BUG-007: Missing `PUT` Method on `AccountSettingsView`
- **Severity**: Medium (REST API Non-Compliance)
- **Module**: `accounts/views.py`
- **Symptom**: Client updating settings via HTTP `PUT` received HTTP 405 Method Not Allowed.
- **Root Cause**: `AccountSettingsView` implemented `patch()` but lacked a `put()` method.
- **Resolution**: Added `def put(self, request): return self.patch(request)` in [`accounts/views.py`](file:///c:/Users/USER/Documents/JustBaddo/accounts/views.py).
- **Verification**: `test_complete_authentication_journey` verified HTTP 200 on `PUT /api/v1/accounts/settings/`.

---

### BUG-008: Playback Telemetry Log Serializer Parameter Mismatch
- **Severity**: Medium (Telemetry Dropped)
- **Module**: `playback/serializers.py`
- **Symptom**: Client posting completed playback telemetry was rejected with HTTP 400 Bad Request.
- **Root Cause**: `PlaybackLogSerializer` strictly required `duration_seconds` and `completed_listen`, while client dispatched `duration_played` and `completed`.
- **Resolution**: Added validation fallback in [`playback/serializers.py`](file:///c:/Users/USER/Documents/JustBaddo/playback/serializers.py) accepting both parameter sets.
- **Verification**: Verified via `test_music_catalogue_and_playback_telemetry_flow`.

---

### BUG-009: Missing Client API Integration Across Frontend Pages
- **Severity**: High (Frontend Isolated from Backend)
- **Module**: `frontend/`
- **Symptom**: Frontend pages did not load `api-client.js` and were unable to communicate with backend APIs.
- **Root Cause**: Phase 1 templates were developed using static demonstration scripts without an API abstraction layer.
- **Resolution**: Created [`frontend/static/js/core/api-client.js`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/core/api-client.js) and injected it across `index.html` and all 22 page templates.
- **Verification**: Tested end-to-end against all 22 page templates.

---

### BUG-010: Serializer Default Boolean Overwrite Masking `completed: True`
- **Severity**: High (Telemetry & Session Invalidation Failed)
- **Module**: `playback/serializers.py`
- **Symptom**: Submitting `completed: True` to `/api/v1/playback/log/` failed to trigger session invalidation and deduplication.
- **Root Cause**: `completed_listen = serializers.BooleanField(default=False)` populated `attrs['completed_listen'] = False` before `validate()` ran, causing `if 'completed_listen' not in attrs` to evaluate to `False`.
- **Resolution**: Updated `validate()` in [`playback/serializers.py`](file:///c:/Users/USER/Documents/JustBaddo/playback/serializers.py) to compute `is_completed = bool(attrs.get('completed_listen') or attrs.get('completed', False))` and assign to both attributes.
- **Verification**: Verified via `test_session_invalidation_after_completion` and `test_duplicate_completion_event_deduplication`.

---

### BUG-011: Privacy Attribute Name Mismatch in `PlaybackService.get_user_history`
- **Severity**: High (HTTP 500 Unhandled Exception)
- **Module**: `playback/services.py`
- **Symptom**: Querying `/api/v1/playback/history/?username=<user>` crashed with `AttributeError: 'AccountSettings' object has no attribute 'history_visibility'`.
- **Root Cause**: `AccountSettings` model stores `private_listening_activity`, while `PlaybackService` looked up `history_visibility`.
- **Resolution**: Changed lookup to `getattr(settings_obj, 'private_listening_activity', False)` in [`playback/services.py`](file:///c:/Users/USER/Documents/JustBaddo/playback/services.py).
- **Verification**: `test_user_history_privacy_guard` passed with HTTP 200 OK.

---

### BUG-012: Hardcoded Active Phase String in Metadata Test
- **Severity**: Low (Test Fragility)
- **Module**: `core/tests.py`
- **Symptom**: `CoreApiTests.test_platform_metadata` failed with `AssertionError: 'Phase 2' not found in 'Phase 6: Authorised Music Streaming & Player Activation'`.
- **Root Cause**: Test hardcoded an expectation for `'Phase 2'` string in platform metadata.
- **Resolution**: Updated assertion to `self.assertIn('Phase', data['data']['active_phase'])` in [`core/tests.py`](file:///c:/Users/USER/Documents/JustBaddo/core/tests.py).
- **Verification**: `test_platform_metadata` passed with HTTP 200 OK.

---

### BUG-013: Unescaped Quotes in Story Card Alt Attributes & Pitch-Black Third-Party Cover Art
- **Severity**: Medium (Visual Regression & Broken Image Placeholder in Browser)
- **Module**: `frontend/static/js/pages/stories-page.js`, `frontend/static/js/pages/music-page.js`, `frontend/static/js/data/catalogue.js`, `frontend/static/js/data/stories-data.js`
- **Symptom**:
  1. On `/pages/stories.html`, the card for `How "Eni Duro" Saved My Faith in Indigenous African Rap` displayed a broken image placeholder rendered with `4How` instead of story cover artwork.
  2. On `/pages/music.html`, the card for debut album `Rapsodi` (2011) appeared as an empty/solid pitch-black container.
- **Root Cause**:
  1. Double quotes in story title `How "Eni Duro" Saved My Faith...` were interpolated directly into `alt="${story.title}"` without HTML attribute escaping, terminating `alt="How "` prematurely, corrupting element attributes, and breaking the `onerror` handler in Chrome.
  2. The Unsplash URL selected for Rapsodi (`photo-1508700115892-45ecd05ae2ad`) was an almost pure black photograph (mean RGB [42, 30, 24]), rendering as an invisible black box on dark-mode card containers.
  3. Lack of dependable, self-contained local vector artwork fallbacks in `frontend/static/images/`.
- **Resolution**:
  1. Authored `escapeAttr()` utility across `stories-page.js`, `music-page.js`, `album-page.js`, `search-page.js`, and `queue.js` to escape quotes, ampersands, and angle brackets.
  2. Generated high-contrast, branded SVG artworks (`rapsodi.svg`, `eni-duro-story.svg`, `default-album-cover.svg`, `default-story-cover.svg`, etc.) in `frontend/static/images/`.
  3. Updated `stories-data.js`, `catalogue.js`, `seed_catalogue.py`, and `index.html` to reference the local SVG assets and bound reliable local fallbacks to all `onerror` handlers.
- **Verification**: Browser requests to `/static/images/albums/rapsodi.svg` and `/static/images/stories/eni-duro-story.svg` return HTTP 200 OK. Rapsodi displays vibrant gold/amber vinyl iconography; Eni Duro story displays high-resolution urban typography; all 62 automated tests pass with 0 failures.
