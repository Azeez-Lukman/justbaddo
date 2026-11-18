
# JUSTBADDO MUSIC ARCHITECTURE

## 1. Purpose

This document defines the technical architecture for the JustBaddo music catalogue and playback system.

The goal is to build a custom music experience that can initially use authorised external streaming providers and eventually support audio hosted and delivered through JustBaddo's own infrastructure.

## 2. Confirmed Requirements

- Free listening at launch, subject to licensing and provider permissions.
- Optional premium features in the future.
- Nigeria and international audiences.
- Custom JustBaddo player interface.
- Comprehensive music catalogue.
- Playlists and listening history.
- Provider-independent playback architecture.
- Future self-hosted streaming capability.

## 3. Recommended Technology Stack

### Frontend
- HTML5
- Tailwind CSS 4
- Vanilla JavaScript
- HTML5 Audio API where permitted by the audio source

### Backend
- Python
- Django
- Django REST Framework where API endpoints are required

### Database
- PostgreSQL

### Supporting Infrastructure
- Redis when required
- Celery for background jobs when required
- Cloud object storage for authorised audio files
- CDN for audio delivery
- Git and GitHub for version control

### Development Approach

Use a modular Django monolith initially.

Avoid unnecessary microservices and complex infrastructure during the early development stages.

## 4. Architectural Principles

1. JustBaddo owns its catalogue metadata and user experience.
2. Audio playback must use an authorised source.
3. The player interface must not depend directly on one provider.
4. Every track must have a playback availability status.
5. Rights and territorial restrictions must be enforced.
6. Audio URLs and provider credentials must not be exposed unnecessarily.
7. The system must support migration to self-hosted streaming.

## 5. Suggested Django Application Structure

```text
justbaddo/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── core/
│   ├── accounts/
│   ├── music/
│   ├── playback/
│   ├── playlists/
│   ├── listening/
│   ├── licensing/
│   ├── notifications/
│   └── moderation/
│
├── templates/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/
├── manage.py
└── requirements.txt
```

The `media/` directory must not become a public storage location for copyrighted recordings without permission.

## 6. Core Components

### Music Catalogue

Responsible for:
- Artists
- Albums
- EPs
- Singles
- Tracks
- Collaborations
- Featured appearances
- Credits
- Release information
- Catalogue sources

### Playback Service

Responsible for:
- Starting playback
- Pausing playback
- Resuming playback
- Seeking
- Track progression
- Playback state
- Provider selection
- Availability checks

### Provider Adapter

Responsible for translating JustBaddo playback requests into provider-specific operations.

Suggested provider structure:

```text
playback/
    providers/
        base.py
        soundcloud.py
        youtube.py
        self_hosted.py
```

Only implement integrations that are permitted by the relevant provider terms and agreements.

### Playlist Service

Responsible for:
- Creating playlists
- Editing playlists
- Adding tracks
- Removing tracks
- Reordering tracks
- Sharing playlists

### Listening History

Responsible for:
- Recently played tracks
- Listening activity
- Playback analytics
- User listening preferences

Listening history should be subject to user privacy controls.

### Licensing Service

Responsible for:
- Rights holder records
- Licence documents
- Territory restrictions
- Permitted uses
- Licence start and expiry dates
- Track-level permissions
- Withdrawal and takedown status

## 7. Database Model Overview

Recommended models:

- Artist
- Album
- Track
- TrackCredit
- MusicProvider
- TrackAvailability
- MusicRights
- RightsHolder
- LicenceAgreement
- Playlist
- PlaylistTrack
- ListeningHistory
- PlaybackEvent

Detailed fields are defined in `JUSTBADDO_CATALOGUE_SCHEMA.md`.

## 8. Track Availability

Every track must have an explicit playback status.

Suggested statuses:

- metadata_only
- provider_available
- self_hosted_available
- restricted
- withdrawn

A track with metadata only must not display an active playback action.

Territory restrictions must be checked before playback.

## 9. Playback Provider Interface

The frontend should communicate with a consistent player interface.

Illustrative JavaScript interface:

```javascript
play(track)
pause()
resume()
seek(seconds)
setVolume(level)
next()
previous()
getCurrentTrack()
getPlaybackState()
```

Provider-specific integrations will implement the operations they support.

Some providers may not permit all operations or may require their own embedded player. The interface must accommodate those differences.

## 10. Playback Flow

1. User selects a track.
2. Frontend requests playback.
3. Backend checks track availability.
4. Backend checks territory restrictions.
5. Backend checks provider and licence permissions.
6. An authorised provider or audio source is selected.
7. Playback begins using the permitted integration.
8. Playback events are recorded where permitted.
9. Listening history is updated according to user settings.

## 11. Future Self-Hosted Architecture

Once direct licensing is secured:

1. Obtain authorised master audio files.
2. Store original files in private object storage.
3. Generate suitable streaming versions.
4. Deliver audio through a CDN.
5. Use short-lived signed access URLs or equivalent controls.
6. Enforce territory and licence restrictions.
7. Record eligible listening activity.
8. Generate royalty and usage reports.

HLS audio delivery may be considered, depending on the selected infrastructure.

## 12. Security Requirements

- Protect provider credentials.
- Never expose private storage credentials in frontend code.
- Validate playback requests.
- Enforce user and territory permissions.
- Use HTTPS.
- Apply rate limits.
- Protect administrative actions.
- Maintain audit logs for licensing changes.
- Secure licence documents.
- Implement takedown procedures.

## 13. Scalability

The architecture should support:
- More users
- More catalogue entries
- More providers
- More territories
- More playlists
- Higher playback traffic
- Self-hosted audio delivery

Do not introduce expensive infrastructure before usage justifies it.

## 14. Important Restrictions

Do not:
- Upload unauthorised MP3 files.
- Circumvent provider playback restrictions.
- Extract audio from YouTube.
- Use undocumented APIs for commercial streaming.
- Assume a streaming subscription grants redistribution rights.
- Promise offline listening without the appropriate rights.

## 15. Definition of Completion

The initial architecture is ready when:

- Music metadata can be stored and searched.
- Track availability can be managed.
- Rights records can be associated with tracks.
- A provider adapter can be configured.
- Playback requests are validated.
- The player can maintain its state across supported page navigation.
- The system can later accept a self-hosted provider without redesigning the catalogue.
