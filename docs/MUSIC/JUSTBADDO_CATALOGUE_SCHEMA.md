
# JUSTBADDO MUSIC CATALOGUE SCHEMA

## 1. Purpose

This document defines how JustBaddo will collect, verify, organise and store Olamide's music catalogue.

The catalogue must be comprehensive, searchable and properly sourced.

Catalogue completeness and playback availability are separate concepts.

A song can appear in the catalogue even when JustBaddo does not yet have permission to stream it.

## 2. Catalogue Categories

The research process should cover:

1. Studio albums
2. Extended plays (EPs)
3. Mixtapes and documented projects
4. Singles
5. Collaborations
6. Featured appearances
7. Remixes
8. Official soundtrack contributions
9. Music videos
10. Official performances
11. Documented special releases

Unreleased, leaked or unauthorised recordings must not be presented as official releases.

## 3. Track Fields

Each track should contain:

| Field | Description |
|---|---|
| title | Official track title |
| slug | URL-friendly identifier |
| release_date | Verified release date |
| album | Associated album or project |
| track_number | Position on original release |
| duration | Verified duration |
| featured_artists | Featured performers |
| producers | Verified producers |
| songwriters | Verified songwriters |
| release_type | Album, single, EP, feature, etc. |
| artwork | Authorised artwork reference |
| source_url | Research source |
| verification_status | Verification state |
| playback_status | Playback permission state |

## 4. Album Fields

- Album title
- Slug
- Release date
- Release type
- Track count
- Description
- Artwork
- Label
- Distributor
- Catalogue source
- Verification status

## 5. Artist and Contributor Records

Create separate records for:
- Main artists
- Featured artists
- Producers
- Songwriters
- Composers
- Other contributors

Avoid putting every contributor into one unstructured text field.

## 6. Research Sources

Potential research sources include:

- Official artist channels.
- Official label announcements.
- Apple Music catalogue listings.
- Spotify catalogue listings.
- YouTube official releases.
- MusicBrainz.
- Discogs.
- Reliable music publications.
- Rights-holder and distributor information.

These sources have different authority levels.

A listing on a streaming service is useful evidence of release information but does not prove that JustBaddo has streaming rights.

## 7. Source Verification

Every important catalogue entry should have a source.

Suggested verification statuses:

- unverified
- partially_verified
- verified
- disputed

Where sources disagree, record the discrepancy instead of silently selecting an uncertain answer.

## 8. Playback Availability

Suggested playback statuses:

- metadata_only
- provider_available
- self_hosted_available
- restricted
- withdrawn

Playback availability should be separate from catalogue verification.

## 9. Suggested Database Relationships

```text
Artist
  |
  |--- Album
  |      |
  |      |--- Track
  |             |
  |             |--- TrackCredit
  |             |--- TrackAvailability
  |             |--- MusicRights
  |
  |--- FeaturedAppearance

Track
  |
  |--- MusicProvider
  |--- ListeningHistory
  |--- PlaylistTrack
```

A track may appear on more than one release or in more than one catalogue context. The data model should avoid unnecessary duplication.

## 10. Research Spreadsheet Structure

Create these sheets:

### Albums
Album title, release date, type, label, source, verification status.

### Tracks
Track title, album, track number, duration, features, producers, source.

### Singles
Title, release date, collaborators, source, verification status.

### Features
Song title, main artist, Olamide's role, release date, source.

### Music Videos
Title, release date, official channel, source link.

### Availability
Track, provider, country, playback status, verification date.

### Missing and Disputed
Unconfirmed releases, conflicting dates, missing credits and research notes.

## 11. Catalogue Rules

- Do not invent release dates.
- Do not invent producers or songwriter credits.
- Do not assume every online upload is official.
- Distinguish original releases from reissues.
- Distinguish lead artist credits from featured appearances.
- Preserve source links.
- Record the date information was verified.
- Never equate catalogue inclusion with streaming permission.

## 12. Completion Criteria

The catalogue is ready for initial product use when:

- Major albums and EPs have been documented.
- Singles have been recorded.
- Featured appearances have been investigated.
- Tracklists have been checked.
- Release information has sources.
- Disputed entries are identified.
- Playback availability is recorded separately.
