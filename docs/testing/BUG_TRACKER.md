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
