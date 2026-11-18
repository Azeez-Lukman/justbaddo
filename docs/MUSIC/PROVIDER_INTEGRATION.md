# JUSTBADDO — PROVIDER INTEGRATION SPECIFICATION

## 1. Overview

This document provides developer guidelines and integration mechanics for each audio provider adapter implemented in JustBaddo:
1. `MockAudioProvider` (Web Audio API Synthesizer)
2. `SoundCloudAudioProvider` (SoundCloud Widget API)
3. `YouTubeAudioProvider` (YouTube IFrame Player API)
4. `SelfHostedAudioProvider` (HTML5 Audio / HLS Stream Engine)

All adapters adhere to the common [`AudioProviderInterface`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/provider-interface.js) contract and are managed centrally by [`AudioProviderManager`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/provider-manager.js).

---

## 2. Provider Adapter Specifications

### 2.1. MockAudioProvider (Web Audio API Synth)
- **File:** [`frontend/static/js/music/mock-provider.js`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/mock-provider.js)
- **Technology:** Web Audio API (`AudioContext`, `GainNode`, `OscillatorNode`).
- **Purpose:** Development preview, automated testing, and zero-copyright offline demonstration.
- **Playback Characteristics:**
  - Generates harmonic frequency pulses tuned to track BPM (tempo) and musical key (e.g. 440 Hz for A, 261.63 Hz for C).
  - Emits real-time progress callbacks (`onTimeUpdate`) on 1-second intervals.
  - Zero external network dependencies; operates seamlessly offline and behind ad-blockers.
- **Capabilities:**
  ```javascript
  {
    providerName: 'web_audio_synth',
    displayName: 'Web Audio API Synth (Zero-Copyright Demo)',
    canSeek: true,
    canChangeVolume: true,
    supportsHeadless: true,
    requiresUserGesture: false,
    isAuthorizedStream: false
  }
  ```

---

### 2.2. SoundCloudAudioProvider (SoundCloud Widget API)
- **File:** [`frontend/static/js/music/soundcloud-provider.js`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/soundcloud-provider.js)
- **Technology:** SoundCloud HTML5 Widget API (`https://w.soundcloud.com/player/api.js`).
- **Purpose:** Streaming official Olamide and YBNL tracks that permit third-party embeds.
- **Integration Architecture:**
  - Injects a concealed host iframe (`#jb-soundcloud-host`) with `allow="autoplay"`.
  - Connects `window.SC.Widget(iframe)` upon DOM initialization.
  - Listens to native events:
    - `SC.Widget.Events.READY`: Retrieves true duration via `widget.getDuration()`.
    - `SC.Widget.Events.PLAY` / `PAUSE`: Synchronizes UI play/pause toggles.
    - `SC.Widget.Events.PLAY_PROGRESS`: Dispatches `currentTime` in seconds.
    - `SC.Widget.Events.FINISH`: Dispatches track completion to advance queue and log telemetry.
- **Capabilities:**
  ```javascript
  {
    providerName: 'soundcloud',
    displayName: 'SoundCloud Official Partner Widget',
    canSeek: true,
    canChangeVolume: true,
    supportsHeadless: false,
    requiresUserGesture: true,
    isAuthorizedStream: true
  }
  ```

---

### 2.3. YouTubeAudioProvider (YouTube IFrame Player API)
- **File:** [`frontend/static/js/music/youtube-provider.js`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/youtube-provider.js)
- **Technology:** YouTube IFrame Player API (`https://www.youtube.com/iframe_api`).
- **Purpose:** Streaming official music videos and visualizers published by YBNL Nation / EMPIRE.
- **Terms of Service Compliance (Section II.D):**
  - YouTube strictly prohibits stripping or separating audio from video streams.
  - The adapter mounts an iframe with video dimensions preserved in `#jb-youtube-host` (or expanded player view), maintaining branding and player controls attribution.
- **Lifecycle & Events:**
  - Automatically loads the YouTube IFrame API script dynamically if not present.
  - Hooks `onReady`, `onStateChange` (`YT.PlayerState.PLAYING`, `PAUSED`, `ENDED`, `BUFFERING`), and `onError`.
  - Polls `getCurrentTime()` on a 1-second timer during playback to drive progress sliders.
- **Capabilities:**
  ```javascript
  {
    providerName: 'youtube',
    displayName: 'YouTube IFrame Player (Official Visualizer)',
    canSeek: true,
    canChangeVolume: true,
    supportsHeadless: false,
    requiresUserGesture: true,
    isAuthorizedStream: true
  }
  ```

---

### 2.4. SelfHostedAudioProvider (HTML5 Audio / HLS Stream Engine)
- **File:** [`frontend/static/js/music/self-hosted-provider.js`](file:///c:/Users/USER/Documents/JustBaddo/frontend/static/js/music/self-hosted-provider.js)
- **Technology:** Native HTML5 Audio (`new Audio()`) with signed token authentication and HLS video/audio media source extensions.
- **Purpose:** Phase 7 direct licensed streaming delivery.
- **Integration Architecture:**
  - Dynamically binds `audioElement.src` to time-limited signed streaming URLs (`https://stream.justbaddo.com/hls/iki-01.m3u8?token=...`).
  - Standard DOM event listeners (`play`, `pause`, `timeupdate`, `waiting`, `ended`, `error`).
- **Capabilities:**
  ```javascript
  {
    providerName: 'self_hosted',
    displayName: 'JustBaddo Direct Licensed CDN Stream',
    canSeek: true,
    canChangeVolume: true,
    supportsHeadless: true,
    requiresUserGesture: false,
    isAuthorizedStream: true
  }
  ```

---

## 3. Provider Error Handling & Graceful Fallback

When an external provider fails (e.g. YouTube video removed, SoundCloud track blocked, or network disconnected):
1. The adapter fires `this.callbacks.onError(err)`.
2. `AudioProviderManager._wrapCallbacks` intercepts the error before it crashes the UI.
3. The manager automatically activates `MockAudioProvider` for that track.
4. A notification toast informs the user: *"Partner stream unavailable. Switched to synthetic demonstration audio."*
5. Playback continues without stalling or dropping the active queue.
