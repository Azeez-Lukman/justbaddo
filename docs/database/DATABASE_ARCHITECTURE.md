# JUSTBADDO — DATABASE ARCHITECTURE SPECIFICATION

## 1. Overview & Architectural Philosophy

The JustBaddo persistent database layer is designed as a relational system powered by **PostgreSQL** and managed through **Django ORM**.

The database architecture directly reflects the 11 modular domain applications established in Phase 2. It prioritizes:
1. **Referential Integrity**: Robust foreign key constraints, explicit deletion behaviors (`CASCADE`, `SET_NULL`), and composite unique constraints preventing data anomalies.
2. **Normalized Discography Representation**: Decoupled modeling of Artists, Albums, Tracks, and Genres, eliminating duplicate metadata entries.
3. **Zero-Copyright Audio Compliance**: No binary audio data, media URLs to unauthorized MP3s, or raw stream blobs are stored. Tracks carry explicit `playback_status` and `RightsRecord` relations.
4. **Precomputed Analytics & Aggregates**: Denormalized counters (e.g. `likes_count`, `votes`) updated transactionally to maintain high read throughput.

```
+-------------------------------------------------------------------------------------------------------+
|                                    POSTGRESQL RELATIONAL SCHEMA                                       |
+-------------------------------------------------------------------------------------------------------+

       [auth_user] <1:1> [accounts_user_profile]
            |      <1:1> [accounts_user_settings]
            |      <1:1> [moderation_user_restrictions]
            |
            +------------< [community_posts] <1:N> [community_comments]
            |                    ^                       ^
            |                    |                       |
            |                    +---< [community_post_likes]
            |
            +------------< [playlists_playlists] <1:N> [playlists_playlist_tracks] >---+
            |                                                                          |
            +------------< [arena_poll_votes] >--- [arena_poll_options] >- [arena_polls]
            |                                                                          |
            +------------< [arena_battle_votes] >- [arena_song_battles] >--------------+
            |                                                                          |
            +------------< [arena_trivia_submissions]                                  |
            |                                                                          |
            +------------< [stories_stories]                                           |
            |                                                                          |
            +------------< [notifications_notifications]                               |
            |                                                                          |
            +------------< [moderation_reports] <1:N> [moderation_actions]             |
            |                                                                          |
            +------------< [playback_listening_history] >------------------------------+
            |                                                                          |
            +------------< [playback_sessions] >---------------------------------------+
                                                                                       |
                                                                                       v
                               [music_albums] <1:N> [music_tracks] <1:1> [licensing_rights_records]
                                     |                     ^
                                     v                     |
                           [music_albums_genres]    [music_artists]
                                     |
                               [music_genres]
```

---

## 2. Domain Entities & Relationships

### A. Accounts Domain
- `auth_user`: Django's core authentication entity managing credentials and session state.
- `accounts_user_profile`: One-to-one extension of `auth_user` storing fan tier (`Day One Disciple`, `OLIC Veteran`, `Voice of the Street Ambassador`), engagement points, avatar, city, and verified status.
- `accounts_user_settings`: One-to-one configuration table managing playback toggles (`auto_advance_queue`, `audio_preview_enabled`) and notification digests.

### B. Music Catalogue Domain
- `music_artists`: Biographical and origin archive for Olamide Adedeji.
- `music_genres`: Canonical genre taxonomies (Afrobeats, Indigenous Yoruba Hip-Hop, Street Rap, etc.).
- `music_albums`: Discography albums and EPs, labeled by release year, type, distributor, and high-resolution artwork.
- `music_tracks`: Individual musical works linked to albums or standalone singles. Features BPM, musical key, producer credits, and explicit playback rights status (`JUSTBADDO_STREAMING`, `AUTHORISED_PROVIDER`, `METADATA_ONLY`, `RESTRICTED`, `WITHDRAWN`).
- `music_timeline_milestones`: Chronological landmark events (2010–2024) with archival source citations.

### C. Playlists Domain
- `playlists_playlists`: User-created and editorial playlists with private/public visibility toggles.
- `playlists_playlist_tracks`: Explicit through-table providing ordered positioning (`order`) and unique constraint `(playlist_id, track_id)`.

### D. Community Domain
- `community_posts`: Discussion threads categorised by discography, lyrics, concerts, or general chat.
- `community_comments`: Threaded responses belonging to posts.
- `community_post_likes`: Unique join table `(post_id, user_id)` preventing duplicate like reactions.
- `community_follows`: Asymmetric social graph `(follower_id, followed_id)`.

### E. Fan Arena Domain
- `arena_polls`: Community inquiries with multiple `arena_poll_options`. Single-vote enforcement via `arena_poll_votes` with composite unique constraint `(poll_id, user_id)`.
- `arena_song_battles`: Head-to-head clashes between two tracks (`song_a` and `song_b`). Votes recorded via `arena_battle_votes` with composite unique constraint `(battle_id, user_id)`.
- `arena_trivia_questions`: Verified discography questions with options JSON, correct index, and educational explanations.
- `arena_trivia_submissions`: User answer sheets, awarded points, and performance records.

### F. Stories Domain
- `stories_stories`: Long-form fan essays and concert memoirs supporting editorial review statuses (`DRAFT`, `PENDING_REVIEW`, `PUBLISHED`, `REJECTED`).

### G. Notifications Domain
- `notifications_notifications`: Fan alerts with categories, unread flags, and target deep links.

### H. Licensing & Rights Domain
- `licensing_rights_records`: Direct one-to-one mapping with `music_tracks` defining copyright ownership, allowable playback modes (`web_audio_synth`, `authorised_provider_embed`), and allowed territories (`GLOBAL`, `NG`, etc.).
- `licensing_rights_inquiries`: Rightsholder outreach desk for licensing proposals, credit corrections, and takedown notices.

### I. Moderation Domain
- `moderation_reports`: Safety flags submitted against posts, comments, stories, or users.
- `moderation_actions`: Audit logs of staff disciplinary decisions (`WARN`, `REMOVE_CONTENT`, `SUSPEND`, `BAN`).
- `moderation_user_restrictions`: One-to-one restriction state on user accounts.

---

## 3. Database Constraints & Integrity Guarantees

1. **Unique Contributor Constraints**:
   - `arena_poll_votes`: `UNIQUE (poll_id, user_id)`
   - `arena_battle_votes`: `UNIQUE (battle_id, user_id)`
   - `community_post_likes`: `UNIQUE (post_id, user_id)`
   - `community_follows`: `UNIQUE (follower_id, followed_id)`
   - `playlists_playlist_tracks`: `UNIQUE (playlist_id, track_id)`
2. **Identification Uniqueness**:
   - Track identifiers (`track_id`), album slugs (`slug`), playlist identifiers (`playlist_id`), post identifiers (`post_id`), and story identifiers (`story_id`) carry database-level unique constraints.
3. **Cascade Rules**:
   - Deleting an album cascades to its constituent tracks and rights records.
   - Deleting a user cascades to their profile, custom playlists, and private comments, but soft-moderated content is preserved where required by moderation logs.
