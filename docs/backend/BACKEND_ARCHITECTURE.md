# JUSTBADDO — BACKEND ARCHITECTURE SPECIFICATION

## 1. Architectural Philosophy: Modular Django Monolith

JustBaddo is engineered as a **Modular Django Monolith**. 

Rather than adopting premature microservices or heavy single-page application frameworks that add deployment friction and distributed state fragility, the platform consolidates all server-side capabilities into one cohesive codebase partitioned into **11 strictly bounded domain applications**.

```
                        +---------------------------------------------+
                        |          Client Layer (Frontend)            |
                        |   HTML5 + Tailwind 4 + Vanilla JS + WebAudio |
                        +---------------------------------------------+
                                               |
                                     HTTP / REST / JSON
                                               v
                        +---------------------------------------------+
                        |        Django Gateway & Security            |
                        |   CorsMiddleware, CSRF, Throttling, Auth    |
                        +---------------------------------------------+
                                               |
       +--------------------+------------------+-------------------+--------------------+
       |                    |                  |                   |                    |
+--------------+    +--------------+    +--------------+    +--------------+    +--------------+
|   accounts   |    |    music     |    |   playback   |    |  playlists   |    |  community   |
| Registration |    | Discography  |    | Provider-Ind |    | Custom User  |    | Feed & Posts |
| Profiles     |    | Track credits|    | Availability |    | Collections  |    | Discussions  |
+--------------+    +--------------+    +--------------+    +--------------+    +--------------+
       |                    |                  |                   |                    |
+--------------+    +--------------+    +--------------+    +--------------+    +--------------+
|    arena     |    |   stories    |    |notifications |    |  licensing   |    |  moderation  |
| Battles/Polls|    | Fan Essays   |    | Real-time    |    | Clearance    |    | Safety &     |
| Trivia Quiz  |    | Submissions  |    | User Alerts  |    | Rights Desk  |    | Reports      |
+--------------+    +--------------+    +--------------+    +--------------+    +--------------+
       |                    |                  |                   |                    |
       +--------------------+------------------+-------------------+--------------------+
                                               |
                        +---------------------------------------------+
                        |         Service & Repository Layer          |
                        |    Business Logic, Rules, Permissions       |
                        +---------------------------------------------+
                                               |
                        +---------------------------------------------+
                        |       Persistence Tier (Phase 3 Prep)       |
                        |     Environment-driven PostgreSQL Engine    |
                        +---------------------------------------------+
```

---

## 2. Domain Applications & Responsibilities

| Application | Core Responsibility | Key Services & Views |
|---|---|---|
| `core` | Shared infrastructure, health check, global exception formatting, pagination, context processors. | `HealthCheckView`, `PlatformMetadataView`, `StandardResultsSetPagination`, `custom_exception_handler` |
| `accounts` | Identity, registration, authentication, member profiles, account settings, password reset. | `AccountService`, `RegisterView`, `LoginView`, `CurrentUserProfileView`, `AccountSettingsView` |
| `music` | Verified Olamide discography archive (albums, EPs, singles, track BPM/key, credits, timeline). | `MusicService`, `AlbumListView`, `AlbumDetailView`, `TrackDetailView`, `CareerTimelineView` |
| `playback` | Provider-independent playback coordinator, availability verification, session tracking, listening logs. | `PlaybackService`, `PlaybackCheckView`, `PlaybackSessionInitView`, `PlaybackLogView` |
| `playlists` | Editorial collections, user custom playlists, track additions, reordering, and privacy controls. | `PlaylistService`, `PlaylistListCreateView`, `PlaylistDetailView`, `PlaylistTrackActionView` |
| `community` | Interactive fan discussions, category tagging, threaded comments, and like reactions. | `CommunityService`, `PostListCreateView`, `PostDetailView`, `PostCommentCreateView`, `PostLikeToggleView` |
| `arena` | Head-to-head song battles, community polls, verified discography trivia scoring, leaderboard. | `ArenaService`, `PollListView`, `SongBattleListView`, `TriviaSubmitView`, `LeaderboardView` |
| `stories` | Long-form fan essays, concert reflections (OLIC history), submission workflow, reader modal data. | `StoriesService`, `StoryListView`, `StoryDetailView`, `StorySubmitView`, `StoryPublishView` |
| `notifications`| Fan alerts, replies, milestone notifications, unread count badges, mark-read operations. | `NotificationService`, `NotificationListView`, `UnreadNotificationCountView`, `MarkNotificationReadView` |
| `licensing` | Track rights clearance registry, territory restrictions, rights status, legal inquiry desk. | `LicensingService`, `RightsRecordListView`, `RightsRecordDetailView`, `RightsInquiryView` |
| `moderation` | Content reporting queue, violation inspection, warning system, suspensions, and bans. | `ModerationService`, `ReportSubmitView`, `ModerationQueueView`, `ModerationActionApplyView` |

---

## 3. Service / Repository Pattern (Phase 2 to Phase 3 Bridge)

To adhere strictly to Phase 2 boundaries without implementing the final PostgreSQL database schema prematurely:

1. **Separation of Presentation and Logic**: Views never contain domain rules; they deserialize requests, call the respective `Service`, and return uniform `api_success()` or `api_error()` envelopes.
2. **Repository Abstraction**: All business operations (such as calculating trivia scores, recording votes, validating playback licenses) reside inside Domain Service classes (`MusicService`, `PlaybackService`, etc.).
3. **Seamless Phase 3 Migration**: In Phase 3, the in-memory data structures inside the Services are swapped for Django ORM QuerySets pointing to PostgreSQL tables without altering API contracts or frontend integration points.

---

## 4. Playback Architecture & Licensing Isolation

JustBaddo is an independent fan community platform and explicitly **does not store or stream unauthorised copyrighted MP3s**. 

The backend enforces this through the `PlaybackService` and `LicensingService`:

```
Client Play Request (/api/v1/playback/session/)
                       |
                       v
         Is track in catalogue?
            /              \
          No               Yes
          /                  \
      404 Not Found       Check playback status
                            /            \
                  METADATA_ONLY /       JUSTBADDO_STREAMING /
                  RESTRICTED            AUTHORISED_PROVIDER
                       |                          |
               403 Forbidden               201 Created
               (Access Denied)       (Returns Provider Type:
                                      'web_audio_synth' or
                                      'external_embed')
```

- Tracks flagged `METADATA_ONLY` reject session initialization with HTTP 403 Forbidden.
- Tracks flagged `JUSTBADDO_STREAMING` return session tokens designating the zero-copyright `web_audio_synth` preview provider.
- Tracks flagged `AUTHORISED_PROVIDER` return licensed partner deeplinks / embed identifiers.

---

## 5. Standardized REST Envelope Contract

All endpoints output a uniform envelope:

### Success Response (HTTP 200 / 201)
```json
{
  "status": "success",
  "message": "Human-readable summary",
  "data": { ... },
  "meta": { "count": 10 }
}
```

### Error Response (HTTP 400 / 401 / 403 / 404 / 429)
```json
{
  "status": "error",
  "code": "VALIDATION_ERROR",
  "message": "Human-readable error summary",
  "errors": {
    "field_name": ["Specific validation error description"]
  }
}
```
