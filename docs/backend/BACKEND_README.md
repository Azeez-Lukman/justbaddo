# JUSTBADDO — BACKEND README

## 1. Overview

The JustBaddo backend is the server-side foundation responsible for powering the platform's functionality, managing application logic, handling user interactions and providing structured data to the frontend.

JustBaddo is an independent music and fan community platform dedicated to Olamide Baddo.

The backend must support the platform's music discovery, user accounts, playlists, community, fan engagement, notifications and administrative functionality.

This is a modular, maintainable software system designed for long-term development.

## 2. Development Phase

**Current phase:** Phase 2 — Backend Development

Development sequence:

1. Frontend Development — Completed
2. Backend Development — Current
3. Database Development — Upcoming
4. Testing and Integration — Upcoming

The backend must be designed with future PostgreSQL integration in mind.

During this phase, establish the backend architecture, application logic, authentication workflows, API endpoints and integration contracts.

Do not implement the final database schema or migrations until Phase 3.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python |
| Backend framework | Django |
| API framework | Django REST Framework |
| Database | PostgreSQL (Phase 3) |
| Frontend integration | Django Templates / REST APIs |
| Authentication | Django Authentication |
| Background processing | Celery (when required) |
| Task queue | Redis (when required) |
| Version control | Git and GitHub |

Architecture: Modular Django Monolith.

Avoid unnecessary microservices and frontend framework changes.

## 4. Backend Applications

The backend is organised into independent Django applications with clearly defined responsibilities.

### core
- Global application configuration.
- Shared utilities.
- Common services.
- Health checks.
- General platform functionality.

### accounts
- User registration.
- Login and logout.
- User profiles.
- Password recovery.
- Account settings.
- Authentication and permissions.

### music
- Artist information.
- Albums.
- Singles.
- Tracks.
- Collaborations.
- Music credits.
- Release information.
- Track availability.

### playback
- Playback session management.
- Playback provider integration.
- Playback access validation.
- Track availability checks.
- Playback restrictions.

### playlists
- Playlist creation.
- Playlist editing.
- Playlist deletion.
- Track management.
- Public and private playlists.

### community
- Community posts.
- Comments.
- Reactions.
- Following.
- Community feed.

### arena
- Fan polls.
- Quizzes.
- Song battles.
- Voting.
- Leaderboards.

### stories
- Fan stories.
- Story submissions.
- Publishing.
- Content moderation.

### notifications
- User notifications.
- Read and unread status.
- Notification preferences.

### licensing
- Music rights records.
- Permission tracking.
- Licensing status.
- Territory restrictions.
- Track availability restrictions.

### moderation
- Content reports.
- Report management.
- User restrictions.
- Moderation actions.
- Administrative review.

## 5. API Architecture

The backend should expose consistent REST API endpoints based on actual frontend requirements.

Suggested endpoint groups:

| Endpoint | Responsibility |
|---|---|
| `/api/accounts/` | Authentication and accounts |
| `/api/profiles/` | User profiles |
| `/api/music/` | Music catalogue |
| `/api/albums/` | Albums |
| `/api/tracks/` | Tracks |
| `/api/playlists/` | Playlists |
| `/api/community/` | Community feed |
| `/api/posts/` | Posts |
| `/api/comments/` | Comments |
| `/api/arena/` | Fan engagement |
| `/api/stories/` | Fan stories |
| `/api/notifications/` | Notifications |

These are proposed endpoint groups. Final routes should follow the frontend's actual data requirements.

Every API endpoint should document:
- Purpose.
- HTTP methods.
- Request structure.
- Response structure.
- Authentication requirements.
- Permissions.
- Validation.
- Error responses.

## 6. Authentication and Permissions

The accounts application should support:

- User registration.
- User login.
- User logout.
- Password reset.
- Profile management.
- Account settings.
- Authenticated access.
- Role-based permissions where required.

Public visitors should be able to browse publicly available content.

Registration should be required for interactive community participation and other protected features.

Administrative permissions must remain separate from ordinary user permissions.

## 7. Music and Playback Architecture

The music system must remain provider-independent.

The backend should support multiple music availability states:

- `metadata_only`
- `provider_available`
- `self_hosted_available`
- `restricted`
- `withdrawn`

Music rights records must distinguish between:

- `unverified`
- `contact_identified`
- `permission_requested`
- `negotiation`
- `licensed`
- `restricted`
- `expired`
- `withdrawn`

The backend must never assume that a recording can be streamed simply because its metadata or audio file is available.

All playback must respect applicable licensing permissions, territories and provider terms.

Unauthorised audio storage, downloading and streaming must not be implemented.

## 8. Security Requirements

Security must be considered throughout development.

Important requirements:

- Secure password handling.
- CSRF protection.
- Input validation.
- Permission enforcement.
- Secure session management.
- Environment variable configuration.
- File upload validation.
- Rate limiting where appropriate.
- Protection against common web vulnerabilities.
- Restricted administrative access.

Never commit passwords, secret keys, API credentials or other sensitive configuration to GitHub.

## 9. Frontend Integration

The completed frontend is the reference for backend development.

The backend must eventually replace demonstration data with real server responses.

Integration should cover:

- Authentication forms.
- User profiles.
- Music catalogue.
- Search.
- Playlists.
- Music availability.
- Community posts.
- Comments and reactions.
- Polls and quizzes.
- Fan stories.
- Notifications.
- User dashboard.

Maintain consistent response structures and clear API contracts.

Avoid unnecessary frontend redesign.

## 10. Development Boundaries

During Phase 2:

**Implement:**
- Django project configuration.
- Application structure.
- URL routing.
- Views.
- Serializers where appropriate.
- Business logic.
- Authentication workflows.
- Permissions.
- Validation.
- API contracts.
- Backend documentation.

**Defer to Phase 3:**
- Final PostgreSQL database schema.
- Database migrations.
- Database relationships and constraints.
- Production database configuration.
- Database seed data.
- Database backup strategy.

Use temporary mock repositories or in-memory data only where appropriate. Do not mistake temporary development implementations for production-ready persistence.

## 11. Documentation

Maintain the following documents:

- `BACKEND_README.md`
- `BACKEND_ARCHITECTURE.md`
- `API_DOCUMENTATION.md`
- `AUTHENTICATION.md`
- `SECURITY.md`

Keep the main project documents updated:

- `TODO.md`
- `PROJECT_STATUS.md`
- `RECOMMENDATION.md`

All documentation must reflect the actual implementation.

## 12. Testing and Quality

Before completing Phase 2, verify:

- Django configuration.
- Application registration.
- URL routing.
- Authentication workflows.
- API request validation.
- Permission enforcement.
- Error handling.
- Business logic.
- Security foundations.
- Frontend integration contracts.

Run applicable Django checks and automated tests.

Do not mark an unimplemented or untested feature as completed.

## 13. Future Development

After backend development, the project will proceed to:

**Phase 3 — Database Development**

This phase will introduce PostgreSQL, final database models, relationships, migrations, seed data and persistent storage.

**Phase 4 — Testing and Integration**

This phase will connect the frontend to the backend, replace demonstration data, test complete user journeys and resolve integration issues.

## 14. Development Principle

Build JustBaddo as a reliable, maintainable and extensible software product.

Prioritise clean architecture, clear responsibilities, secure implementation and consistency between the frontend and backend.

Do not introduce unnecessary complexity.

Every implementation decision should support the long-term stability and growth of JustBaddo.