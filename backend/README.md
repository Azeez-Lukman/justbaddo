# JUSTBADDO — BACKEND MONOLITH

Welcome to the backend foundation for **JustBaddo**, an independent music discovery, discography archiving, and fan community platform dedicated to Olamide Baddo.

---

## 1. Quick Start

### Prerequisites
- Python 3.12+ (or Python 3.14)
- Virtual Environment activated (`.venv`)
- Django 6.1.3 + Django REST Framework

### Running Server
```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run system checks
python manage.py check

# Run automated tests
python manage.py test

# Start development server
python manage.py runserver
```

---

## 2. Backend Application Layout

The backend is built as a **Modular Django Monolith** divided into 11 distinct applications:

1. **`core`**: Global configuration, health check (`/api/v1/health/`), platform metadata, pagination, custom exception formatting, and frontend template routing.
2. **`accounts`**: Registration, authentication, user profiles, settings, and password recovery (`/api/v1/accounts/`).
3. **`music`**: Verified Olamide discography archive (10 studio albums, EPs, singles, track BPM/key, and credits) (`/api/v1/music/`).
4. **`playback`**: Provider-independent playback coordinator, rights validation, and listening logs (`/api/v1/playback/`).
5. **`playlists`**: User playlists and curated editorial collections (`/api/v1/playlists/`).
6. **`community`**: Interactive fan discussion boards, category tagging, comments, and like reactions (`/api/v1/community/`).
7. **`arena`**: Fan Arena song battles, polls, trivia challenge runner, and leaderboard (`/api/v1/arena/`).
8. **`stories`**: Fan editorial essays, concert reflections (OLIC history), and submissions (`/api/v1/stories/`).
9. **`notifications`**: Member notifications, unread counters, and mark-as-read actions (`/api/v1/notifications/`).
10. **`licensing`**: Music rights clearance records, territory restrictions, and legal inquiry desk (`/api/v1/licensing/`).
11. **`moderation`**: Content reporting queue, user warnings, suspensions, and safety actions (`/api/v1/moderation/`).

---

## 3. Detailed Documentation

Detailed architectural and developer guides are located in `docs/backend/`:

- [Backend Architecture Specification](file:///c:/Users/USER/Documents/JustBaddo/docs/backend/BACKEND_ARCHITECTURE.md)
- [REST API Documentation (v1)](file:///c:/Users/USER/Documents/JustBaddo/docs/backend/API_DOCUMENTATION.md)
- [Authentication & Access Control](file:///c:/Users/USER/Documents/JustBaddo/docs/backend/AUTHENTICATION.md)
- [Security Architecture & Threat Mitigation](file:///c:/Users/USER/Documents/JustBaddo/docs/backend/SECURITY.md)
- [Backend README Overview](file:///c:/Users/USER/Documents/JustBaddo/docs/backend/BACKEND_README.md)
