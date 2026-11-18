# JUSTBADDO — PROVIDER-INDEPENDENT PLAYBACK ARCHITECTURE

## 1. Architectural Philosophy

The JustBaddo playback architecture decouples **music discovery and user experience** from **audio stream delivery**. 

The core music player never binds to a proprietary streaming SDK directly. Instead, a clean provider interface layer abstracts playback primitives, allowing the platform to dynamically route tracks to authorized external embeds (SoundCloud, YouTube), synthetic preview generators (Web Audio API), or future direct licensed CDN streams (HLS/DASH) without altering any user interface components.

---

## 2. End-to-End System Architecture

```mermaid
flowchart TD
    subgraph Frontend["Frontend Player Runtime"]
        UI["Persistent Player Bar & Expanded Modal"] --> PlayerCtrl["JustBaddoPlayer (Controller)"]
        PlayerCtrl --> Manager["AudioProviderManager (Factory / Fallback Orchestrator)"]
        
        Manager --> Synth["MockAudioProvider (Web Audio API Synth)"]
        Manager --> SC["SoundCloudAudioProvider (Widget API)"]
        Manager --> YT["YouTubeAudioProvider (IFrame Player API)"]
        Manager --> CDN["SelfHostedAudioProvider (HTML5 Audio / HLS)"]
        
        PlayerCtrl -.->|Session Request & Telemetry| ApiClient["JustBaddoApi.playback"]
    end

    subgraph Backend["Django Monolith (Playback & Licensing Services)"]
        ApiClient --> Views["PlaybackCheckView & PlaybackSessionInitView"]
        Views --> PlaybackSvc["PlaybackService"]
        PlaybackSvc --> LicensingSvc["LicensingService"]
        LicensingSvc --> DB_Rights[("licensing_rights_records")]
        LicensingSvc --> DB_Tracks[("music_tracks")]
        PlaybackSvc --> DB_Sessions[("playback_sessions")]
        PlaybackSvc --> DB_History[("playback_listening_history")]
    end
```

---

## 3. Playback Availability State Machine

Every track in the catalogue is evaluated against 5 discrete availability states. Server-side validation guarantees that a client cannot trigger playback on an ineligible recording:

```mermaid
stateDiagram-v2
    [*] --> CatalogueEvaluation
    
    CatalogueEvaluation --> Withdrawn: track.status == WITHDRAWN or rights.status == withdrawn
    CatalogueEvaluation --> Restricted: territory mismatch or expired date or tier restricted
    CatalogueEvaluation --> MetadataOnly: rights unverified or status == METADATA_ONLY
    CatalogueEvaluation --> SelfHostedAvailable: master & composition rights cleared & approved
    CatalogueEvaluation --> ProviderAvailable: authorized external partner or synthetic pulse

    Withdrawn --> BlockedState: User notified ("Withdrawn by rightsholder")
    Restricted --> BlockedState: User notified ("Territory restricted")
    MetadataOnly --> NonPlayableState: User explores credits/tracklist only
    SelfHostedAvailable --> PlayState: Streams via JustBaddo CDN
    ProviderAvailable --> PlayState: Streams via Partner Embed / Synth
```

### State Specifications

| State | Definition | Server Session Issued? | Frontend UI Player Behavior |
|---|---|---|---|
| `metadata_only` | Track metadata is catalogued, but audio rights are not cleared for web streaming. | **No (HTTP 403 / can_play: false)** | Gray badge `METADATA ONLY`. Track can be inspected for credits, lyrics, and BPM, but play button is disabled. |
| `provider_available` | Audio is cleared for streaming via an authorized third-party partner embed (SoundCloud/YouTube) or synthetic pulse. | **Yes (HTTP 201 Created)** | Amber badge `AUTHORISED PROVIDER`. Audio plays seamlessly through active adapter. |
| `self_hosted_available` | Direct master and mechanical streaming rights cleared and approved by rightsholders. | **Yes (HTTP 201 Created)** | Emerald badge `DIRECT LICENSED`. High-fidelity audio delivered via HTML5 Audio / HLS pipeline. |
| `restricted` | Track playback is prohibited in client's geographic territory, licensing period expired, or tier restricted. | **No (HTTP 403 / can_play: false)** | Rose badge `RESTRICTED`. Toast warning displayed: *"Recording not licensed in your territory."* |
| `withdrawn` | Track has been formally pulled from digital streaming by rightsholders or legal representatives. | **No (HTTP 403 / can_play: false)** | Red badge `WITHDRAWN`. Play button locked; explanatory notice displayed. |

---

## 4. Playback Session & Telemetry Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor User as Fan / Listener
    participant Player as JustBaddoPlayer
    participant Manager as AudioProviderManager
    participant Backend as Django Playback API
    participant DB as PostgreSQL 18
    
    User->>Player: Clicks "Play" on Track
    Player->>Backend: POST /api/v1/playback/session/ (track_id, territory)
    Backend->>DB: Query Track & RightsRecord
    DB-->>Backend: Status, Territories, Expiration, Provider
    
    alt Track Restricted or Expired
        Backend-->>Player: HTTP 403 Forbidden ("Licensing restricted")
        Player->>User: Displays Warning Toast & Updates Badge
    else Track Cleared for Playback
        Backend->>DB: Insert PlaybackSession (session_id, is_valid=True)
        Backend-->>Player: HTTP 201 Created (session_id, provider, capabilities)
        Player->>Manager: loadTrack(track, sessionData)
        Manager->>Manager: Selects Provider Adapter & Mounts Frame
        Manager-->>Player: onPlay event
        Player-->>User: Plays Audio & Updates Progress Slider
    end
    
    User->>Player: Listens to track until completion
    Manager-->>Player: onEnded event
    Player->>Backend: POST /api/v1/playback/log/ (track_id, session_id, completed=True)
    Backend->>DB: Check Deduplication (last 60s) & Invalidate Session
    Backend->>DB: Insert ListeningHistory (user, track, duration)
    Backend-->>Player: HTTP 200 OK ("Listening progress recorded")
    Player->>Player: Advances to next track in Queue
```

---

## 5. Graceful Provider Fallback Hierarchy

To ensure the listener's session is never terminated by external network failures or browser extensions:
1. `AudioProviderManager` initializes the requested external provider (`SoundCloud` or `YouTube`).
2. If the provider iframe triggers `onError` (or fails to load within 2.5 seconds), the manager automatically catches the exception.
3. The manager logs the error and dynamically falls back to `MockAudioProvider` (Web Audio API synth).
4. The user receives a gentle notification toast: *"Partner stream unavailable. Switched to synthetic demonstration audio."*
5. The queue continues advancing without freezing the UI player bar.
