# JUSTBADDO — RELATIONAL DATABASE SCHEMA SPECIFICATION

---

## 1. Accounts Tables

### `accounts_user_profile`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal profile ID |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `UNIQUE`, `NOT NULL` | Owning user reference |
| `display_name` | `VARCHAR(50)` | `NOT NULL` | Public name |
| `bio` | `VARCHAR(500)` | `BLANK` | User biography |
| `avatar_url` | `VARCHAR(500)` | `BLANK` | Avatar CDN image URL |
| `city` | `VARCHAR(100)` | `DEFAULT 'Lagos, Nigeria'` | User city/origin |
| `favorite_era`| `VARCHAR(100)` | `DEFAULT 'Carpe Diem (2020)'`| Favorite Olamide album/era |
| `fan_tier` | `VARCHAR(50)` | `DEFAULT 'Day One Disciple'` | Engagement tier badge |
| `points` | `INTEGER` | `CHECK (points >= 0)`, `DEFAULT 150` | Fan prestige points |
| `is_verified` | `BOOLEAN` | `DEFAULT FALSE` | Verified account status |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Profile creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Last update timestamp |

### `accounts_user_settings`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal settings ID |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `UNIQUE`, `NOT NULL` | Owning user reference |
| `auto_advance_queue` | `BOOLEAN` | `DEFAULT TRUE` | Autoplay next track in queue |
| `audio_preview_enabled` | `BOOLEAN` | `DEFAULT TRUE` | Enable Web Audio synth preview |
| `email_notifications` | `BOOLEAN` | `DEFAULT TRUE` | Email notifications toggle |
| `community_activity_digest`| `BOOLEAN`| `DEFAULT TRUE` | Weekly community digest toggle |
| `private_listening_activity`| `BOOLEAN`| `DEFAULT FALSE` | Hide listening history on profile |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Last modification timestamp |

---

## 2. Music Catalogue Tables

### `music_artists`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal artist ID |
| `name` | `VARCHAR(100)` | `NOT NULL` | Legal / full name |
| `stage_name` | `VARCHAR(100)` | `DEFAULT 'Olamide'` | Stage identity |
| `slug` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | URL slug identifier |
| `origin` | `VARCHAR(100)` | `DEFAULT 'Bariga, Lagos, Nigeria'` | Geographic origin |
| `bio` | `TEXT` | `BLANK` | Biographical article |
| `image_url` | `VARCHAR(500)` | `BLANK` | Artist portrait URL |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Record creation timestamp |

### `music_genres`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal genre ID |
| `name` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Genre title |
| `slug` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | URL slug |

### `music_albums`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal album ID |
| `title` | `VARCHAR(150)` | `NOT NULL` | Album title |
| `slug` | `VARCHAR(150)` | `UNIQUE`, `NOT NULL` | URL slug identifier |
| `album_type` | `VARCHAR(30)` | `DEFAULT 'Studio Album'` | `Studio Album` \| `EP` \| `Compilation` |
| `release_year` | `INTEGER` | `CHECK (release_year >= 0)` | Release calendar year |
| `release_date` | `VARCHAR(50)` | `BLANK` | Formatted release date |
| `cover_art` | `VARCHAR(500)` | `NOT NULL` | Album artwork URL |
| `label` | `VARCHAR(100)` | `DEFAULT 'YBNL Nation'` | Record label |
| `distributor` | `VARCHAR(100)` | `DEFAULT 'EMPIRE'` | Primary distributor |
| `description` | `TEXT` | `NOT NULL` | Editorial album review |
| `featured_artists_text` | `VARCHAR(300)` | `BLANK` | Comma-separated featured guests |
| `producers_text` | `VARCHAR(300)` | `BLANK` | Comma-separated primary producers |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Record modification timestamp |

### `music_tracks`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal track ID |
| `album_id` | `BIGINT` | `FOREIGN KEY (music_albums.id)`, `NULLABLE` | Parent album reference (null for singles) |
| `track_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `iki-01`) |
| `title` | `VARCHAR(150)` | `NOT NULL` | Track title |
| `track_number` | `INTEGER` | `DEFAULT 1` | Track sequencing position |
| `duration` | `VARCHAR(10)` | `DEFAULT '3:00'` | Formatted duration (`mm:ss`) |
| `duration_seconds`| `INTEGER` | `CHECK (duration_seconds >= 0)` | Exact length in seconds |
| `featured` | `VARCHAR(200)` | `BLANK` | Featured guest artists |
| `producer` | `VARCHAR(100)` | `BLANK` | Music producer |
| `bpm` | `INTEGER` | `NULLABLE` | Beats Per Minute tempo |
| `musical_key` | `VARCHAR(10)` | `BLANK` | Key signature (e.g. `Am`, `C#m`) |
| `playback_status` | `VARCHAR(30)`| `DEFAULT 'JUSTBADDO_STREAMING'` | Rights availability status |
| `is_playable` | `BOOLEAN` | `DEFAULT TRUE` | Playback authorization flag |
| `cover_art` | `VARCHAR(500)` | `BLANK` | Track artwork URL |
| `composer` | `VARCHAR(150)` | `DEFAULT 'Olamide Adedeji'` | Songwriter / composer credit |
| `recording_location`| `VARCHAR(100)`| `DEFAULT 'Lagos, Nigeria'` | Studio location |
| `release_year` | `INTEGER` | `DEFAULT 2024` | Release year |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |

### `music_timeline_milestones`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Milestone ID |
| `year` | `INTEGER` | `CHECK (year >= 0)` | Chronological year |
| `date` | `VARCHAR(50)` | `NOT NULL` | Landmark date |
| `title` | `VARCHAR(200)` | `NOT NULL` | Milestone headline |
| `category` | `VARCHAR(50)` | `NOT NULL` | Milestone category tag |
| `description` | `TEXT` | `NOT NULL` | Milestone historical prose |
| `badge` | `VARCHAR(50)` | `NOT NULL` | Badge label |
| `citation` | `VARCHAR(200)` | `NOT NULL` | Historical publication source |
| `order` | `INTEGER` | `DEFAULT 0` | Ordering within the same year |

---

## 3. Playback Tables

### `playback_sessions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Session ID |
| `session_id` | `VARCHAR(64)` | `UNIQUE`, `NOT NULL` | Public session token |
| `track_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `NOT NULL` | Track played |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NULLABLE` | Listening user |
| `provider` | `VARCHAR(50)` | `DEFAULT 'web_audio_synth'` | Audio provider |
| `device_type`| `VARCHAR(50)` | `DEFAULT 'web_browser'` | Client device |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Session start timestamp |

### `playback_listening_history`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | History record ID |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Listening user |
| `track_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `NOT NULL` | Track played |
| `duration_seconds`| `INTEGER` | `CHECK (duration_seconds >= 0)` | Elapsed listen duration |
| `completed` | `BOOLEAN` | `DEFAULT FALSE` | Complete listen flag |
| `listened_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |

---

## 4. Playlists Tables

### `playlists_playlists`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal playlist ID |
| `playlist_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `pl-editorial-01`) |
| `title` | `VARCHAR(150)` | `NOT NULL` | Playlist name |
| `description` | `TEXT` | `BLANK` | Playlist description |
| `creator_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Owning user |
| `is_editorial`| `BOOLEAN` | `DEFAULT FALSE` | Curated editorial playlist flag |
| `is_private` | `BOOLEAN` | `DEFAULT FALSE` | Private collection toggle |
| `cover_image` | `VARCHAR(500)` | `BLANK` | Playlist cover image |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Created timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Last update timestamp |

### `playlists_playlist_tracks`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Association ID |
| `playlist_id` | `BIGINT` | `FOREIGN KEY (playlists_playlists.id)`, `NOT NULL` | Parent playlist |
| `track_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `NOT NULL` | Included track |
| `order` | `INTEGER` | `DEFAULT 0` | Sequencing index |
| `added_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Insertion timestamp |
*Composite Constraint:* `UNIQUE (playlist_id, track_id)`

---

## 5. Community Tables

### `community_posts`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Internal post ID |
| `post_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `post-01`) |
| `author_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Topic author |
| `category` | `VARCHAR(50)` | `NOT NULL` | Category channel |
| `title` | `VARCHAR(200)` | `NOT NULL` | Discussion headline |
| `content` | `TEXT` | `NOT NULL` | Full discussion prose |
| `likes_count`| `INTEGER` | `CHECK (likes_count >= 0)`, `DEFAULT 0` | Cached likes count |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Post creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Last edit timestamp |

### `community_comments`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Comment ID |
| `comment_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `comm-01`) |
| `post_id` | `BIGINT` | `FOREIGN KEY (community_posts.id)`, `NOT NULL` | Parent discussion post |
| `author_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Comment author |
| `content` | `TEXT` | `NOT NULL` | Comment prose |
| `likes_count`| `INTEGER` | `DEFAULT 0` | Cached likes count |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Creation timestamp |

### `community_post_likes`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Like ID |
| `post_id` | `BIGINT` | `FOREIGN KEY (community_posts.id)`, `NOT NULL` | Post reference |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Liking user |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Like timestamp |
*Composite Constraint:* `UNIQUE (post_id, user_id)`

---

## 6. Fan Arena Tables

### `arena_polls`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Poll ID |
| `poll_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `poll-01`) |
| `question` | `VARCHAR(255)` | `NOT NULL` | Poll inquiry headline |
| `category` | `VARCHAR(100)` | `NOT NULL` | Arena category tag |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Voting availability toggle |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Creation timestamp |

### `arena_poll_options`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Option ID |
| `poll_id` | `BIGINT` | `FOREIGN KEY (arena_polls.id)`, `NOT NULL` | Parent poll |
| `option_id` | `VARCHAR(50)` | `NOT NULL` | Identifier (e.g. `opt-01`) |
| `text` | `VARCHAR(200)` | `NOT NULL` | Option label |
| `votes` | `INTEGER` | `DEFAULT 0` | Tally of votes |

### `arena_poll_votes`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Ballot ID |
| `poll_id` | `BIGINT` | `FOREIGN KEY (arena_polls.id)`, `NOT NULL` | Poll voted on |
| `option_id` | `BIGINT` | `FOREIGN KEY (arena_poll_options.id)`, `NOT NULL`| Option chosen |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NULLABLE` | Voter (null for anon) |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Vote timestamp |
*Composite Constraint:* `UNIQUE (poll_id, user_id)`

### `arena_song_battles`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Battle ID |
| `battle_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Identifier (e.g. `battle-01`) |
| `title` | `VARCHAR(200)` | `NOT NULL` | Battle clash headline |
| `category` | `VARCHAR(100)` | `NOT NULL` | Clash category tag |
| `song_a_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `NOT NULL` | Track A contender |
| `song_b_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `NOT NULL` | Track B contender |
| `song_a_votes`| `INTEGER` | `DEFAULT 0` | Track A votes |
| `song_b_votes`| `INTEGER` | `DEFAULT 0` | Track B votes |
| `is_active` | `BOOLEAN` | `DEFAULT TRUE` | Live voting toggle |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Creation timestamp |

### `arena_battle_votes`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Ballot ID |
| `battle_id` | `BIGINT` | `FOREIGN KEY (arena_song_battles.id)`, `NOT NULL`| Battle clash |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NULLABLE` | Voter |
| `selected_song`| `VARCHAR(10)` | `NOT NULL` | `song_a` \| `song_b` |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Vote timestamp |
*Composite Constraint:* `UNIQUE (battle_id, user_id)`

### `arena_trivia_questions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Question ID |
| `question_id`| `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Identifier (e.g. `q1`) |
| `question` | `VARCHAR(300)` | `NOT NULL` | Challenge prompt |
| `options` | `JSONB` | `NOT NULL` | Multiple choice string array |
| `correct_index`| `INTEGER` | `NOT NULL` | Zero-based index of correct answer |
| `explanation`| `TEXT` | `NOT NULL` | Historical context |
| `points` | `INTEGER` | `DEFAULT 50` | Award points |
| `order` | `INTEGER` | `DEFAULT 0` | Sequence |

---

## 7. Fan Stories Tables

### `stories_stories`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Story ID |
| `story_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `story-01`) |
| `author_user_id`| `INTEGER`| `FOREIGN KEY (auth_user.id)`, `NULLABLE` | Author reference |
| `author_name`| `VARCHAR(100)`| `NOT NULL` | Author display name |
| `author_role`| `VARCHAR(100)`| `DEFAULT 'Community Member'` | Author credential role |
| `title` | `VARCHAR(200)`| `NOT NULL` | Essay headline |
| `excerpt` | `TEXT` | `NOT NULL` | Preview teaser |
| `content` | `TEXT` | `NOT NULL` | Full story HTML body |
| `read_time` | `VARCHAR(30)` | `DEFAULT '5 min read'` | Reading duration |
| `cover_image`| `VARCHAR(500)`| `BLANK` | Cover photo URL |
| `tags` | `JSONB` | `DEFAULT '[]'` | Tag list |
| `status` | `VARCHAR(20)` | `DEFAULT 'PUBLISHED'` | `DRAFT` \| `PENDING_REVIEW` \| `PUBLISHED` \| `REJECTED` |
| `likes_count`| `INTEGER` | `DEFAULT 0` | Likes tally |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |

---

## 8. Notifications Tables

### `notifications_notifications`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Alert ID |
| `notification_id`| `VARCHAR(50)`| `UNIQUE`, `NOT NULL`| Identifier (e.g. `notif-01`) |
| `recipient_id`| `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Recipient user |
| `title` | `VARCHAR(150)`| `NOT NULL` | Notification headline |
| `message` | `TEXT` | `NOT NULL` | Notification summary |
| `category` | `VARCHAR(50)` | `DEFAULT 'System'` | `Arena` \| `Community` \| `Music` \| `System` |
| `is_read` | `BOOLEAN` | `DEFAULT FALSE` | Read status |
| `action_url` | `VARCHAR(255)`| `BLANK` | Navigation URL |
| `icon` | `VARCHAR(50)` | `DEFAULT 'bell'` | Lucide icon name |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Alert timestamp |

---

## 9. Licensing Tables

### `licensing_rights_records`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Clearance record ID |
| `track_id` | `BIGINT` | `FOREIGN KEY (music_tracks.id)`, `UNIQUE`, `NOT NULL` | Musical work |
| `rightsholder_label`| `VARCHAR(150)`| `DEFAULT 'YBNL Nation / EMPIRE'` | Master rights owner |
| `licensing_status` | `VARCHAR(30)` | `DEFAULT 'contact_identified'` | Clearance workflow state |
| `territories_allowed`| `JSONB` | `DEFAULT '[]'` | Allowed territory codes |
| `allowed_playback_modes`| `JSONB`| `DEFAULT '[]'` | Allowed delivery modes |
| `disclaimer` | `TEXT` | `BLANK` | Copyright notice prose |

### `licensing_rights_inquiries`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Inquiry ID |
| `inquiry_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Reference tracking ID |
| `claimant_name`| `VARCHAR(100)`| `NOT NULL` | Representative contact |
| `organization`| `VARCHAR(150)`| `NOT NULL` | Entity name |
| `email` | `VARCHAR(254)`| `NOT NULL` | Contact email |
| `track_or_album`| `VARCHAR(200)`| `NOT NULL` | Target catalogue item |
| `inquiry_type`| `VARCHAR(50)` | `NOT NULL` | Outreach classification |
| `message` | `TEXT` | `NOT NULL` | Formal legal message |
| `status` | `VARCHAR(30)` | `DEFAULT 'PENDING_LEGAL_REVIEW'`| Processing status |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Submission timestamp |

---

## 10. Moderation Tables

### `moderation_reports`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Report ID |
| `report_id` | `VARCHAR(50)` | `UNIQUE`, `NOT NULL` | Public identifier (e.g. `rep-001`) |
| `reporter_id`| `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NULLABLE` | Reporting user |
| `target_type`| `VARCHAR(30)` | `NOT NULL` | `POST` \| `COMMENT` \| `USER` \| `STORY` |
| `target_id` | `VARCHAR(50)` | `NOT NULL` | ID of reported resource |
| `reason` | `VARCHAR(50)` | `NOT NULL` | Violation reason code |
| `details` | `TEXT` | `BLANK` | Report explanation |
| `status` | `VARCHAR(30)` | `DEFAULT 'PENDING'` | `PENDING` \| `INVESTIGATING` \| `RESOLVED` \| `DISMISSED` |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Submission timestamp |

### `moderation_actions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Action ID |
| `report_id` | `BIGINT` | `FOREIGN KEY (moderation_reports.id)`, `NOT NULL`| Target report |
| `moderator_id`| `INTEGER` | `FOREIGN KEY (auth_user.id)`, `NOT NULL` | Actioning staff user |
| `action` | `VARCHAR(30)` | `NOT NULL` | Sanction type code |
| `notes` | `TEXT` | `BLANK` | Internal staff notes |
| `created_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |

### `moderation_user_restrictions`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `BIGINT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Restriction ID |
| `user_id` | `INTEGER` | `FOREIGN KEY (auth_user.id)`, `UNIQUE`, `NOT NULL` | Targeted user |
| `is_suspended`| `BOOLEAN` | `DEFAULT FALSE` | Temporary suspension |
| `is_banned` | `BOOLEAN` | `DEFAULT FALSE` | Permanent expulsion |
| `warnings_count`| `INTEGER` | `DEFAULT 0` | Cumulative warning strikes |
| `reason` | `TEXT` | `BLANK` | Sanction justification |
| `updated_at` | `TIMESTAMPTZ` | `DEFAULT NOW()` | Timestamp |
