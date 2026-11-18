# JUSTBADDO — PLAYBACK REST API SPECIFICATION

## 1. Overview

The JustBaddo Playback REST API handles track availability verification, licensed playback session creation, and listening history telemetry logging.

All endpoints adhere to the unified JustBaddo API envelope format:
```json
{
  "status": "success",
  "message": "Human-readable status summary.",
  "data": {},
  "meta": {}
}
```

---

## 2. Endpoints Reference

### 2.1. Check Track Availability & Rights
- **Endpoint:** `GET /api/v1/playback/check/<track_id>/`
- **Permissions:** `AllowAny`
- **Query Parameters:**
  - `territory` (string, optional, default: `'NG'`): ISO 2-letter country code.
- **Success Response (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "Playable via developer synthetic preview pulse (Web Audio API).",
    "data": {
      "exists": true,
      "track_id": "iki-01",
      "title": "Metaverse",
      "can_play": true,
      "status": "JUSTBADDO_STREAMING",
      "availability_state": "provider_available",
      "rights_status": "licensed",
      "rightsholder": "YBNL Nation / EMPIRE",
      "provider": "web_audio_synth",
      "provider_track_id": "iki-01",
      "provider_embed_url": "",
      "territory": "NG",
      "message": "Playable via developer synthetic preview pulse (Web Audio API).",
      "capabilities": {
        "provider_name": "web_audio_synth",
        "display_name": "Web Audio API Synth (Zero-Copyright Demo)",
        "can_seek": true,
        "can_change_volume": true,
        "supports_headless": true,
        "requires_user_gesture": false,
        "is_authorized_stream": false
      },
      "is_synthetic_preview": true
    }
  }
  ```
- **Error Response (`404 NOT FOUND`):**
  ```json
  {
    "status": "error",
    "message": "Track does not exist in catalogue.",
    "code": "TRACK_NOT_FOUND"
  }
  ```

---

### 2.2. Initialize Playback Session
- **Endpoint:** `POST /api/v1/playback/session/`
- **Permissions:** `AllowAny` (Associates session with `request.user` if authenticated)
- **Request Body:**
  ```json
  {
    "track_id": "iki-01",
    "territory": "NG",
    "client_provider": "web_audio_synth",
    "device_type": "web_browser"
  }
  ```
- **Success Response (`201 CREATED`):**
  ```json
  {
    "status": "success",
    "message": "Playback session initialized.",
    "data": {
      "session_id": "play-sess-e8a1b2c3d4f5",
      "track_id": "iki-01",
      "title": "Metaverse",
      "provider": "web_audio_synth",
      "provider_track_id": "iki-01",
      "provider_embed_url": "",
      "territory": "NG",
      "device": "web_browser",
      "availability_state": "provider_available",
      "capabilities": {
        "can_seek": true,
        "can_change_volume": true,
        "supports_headless": true,
        "requires_user_gesture": false
      },
      "started_at": "2026-11-18T14:00:00Z",
      "status": "ACTIVE"
    }
  }
  ```
- **Error Response (`403 FORBIDDEN` - Licensing Restriction):**
  ```json
  {
    "status": "error",
    "message": "Recording is not licensed for playback in territory: US.",
    "code": "PLAYBACK_RESTRICTED"
  }
  ```

---

### 2.3. Log Playback Telemetry
- **Endpoint:** `POST /api/v1/playback/log/`
- **Permissions:** `AllowAny`
- **Request Body:**
  ```json
  {
    "track_id": "iki-01",
    "session_id": "play-sess-e8a1b2c3d4f5",
    "duration_seconds": 167,
    "completed": true,
    "playback_event": "completed",
    "client_timestamp": "2026-11-18T14:02:47Z"
  }
  ```
- **Success Response (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "Listening progress recorded.",
    "data": {
      "id": "hist-42",
      "track_id": "iki-01",
      "username": "baddofan99",
      "duration_seconds": 167,
      "completed": true,
      "event": "completed",
      "timestamp": "2026-11-18T14:02:48Z"
    }
  }
  ```
- **Deduplication Response (`200 OK` - Duplicate Suppressed):**
  ```json
  {
    "status": "success",
    "message": "Listening progress recorded.",
    "data": {
      "status": "duplicate_suppressed",
      "message": "Duplicate completion event suppressed.",
      "track_id": "iki-01",
      "username": "baddofan99"
    }
  }
  ```

---

### 2.4. Retrieve Listening History
- **Endpoint:** `GET /api/v1/playback/history/?username=<username>`
- **Permissions:** `AllowAny` (Privacy rules enforced server-side)
- **Success Response (`200 OK`):**
  ```json
  {
    "status": "success",
    "message": "Success",
    "data": [
      {
        "id": "hist-42",
        "track_id": "iki-01",
        "title": "Metaverse",
        "album_title": "Ikigai / 生き甲斐, Vol. 1",
        "duration_seconds": 167,
        "completed": true,
        "event": "completed",
        "timestamp": "2026-11-18T14:02:48Z"
      }
    ],
    "meta": {
      "count": 1
    }
  }
  ```
- *Note:* If the target user has configured `private_listening_activity = True` in their Account Settings, requesting their history returns an empty list (`[]`) unless the authenticated requester is the user themselves.
