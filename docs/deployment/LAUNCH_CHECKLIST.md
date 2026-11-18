# JUSTBADDO — PRE-FLIGHT LAUNCH READINESS CHECKLIST

## 1. Overview

This checklist serves as the authoritative gatekeeper before JustBaddo is officially opened to public internet traffic. No launch will be declared complete without every mandatory item verified or formally categorized as an accepted operational constraint.

---

## 2. Infrastructure & Technical Verification Checklist

| Domain | Item | Verification Method | Status |
|---|---|---|---|
| **Server & OS** | Production Linux VPS / Docker host provisioned | System uptime & CPU/RAM allocation verified | Prepared |
| **Runtime** | Python 3.12+ runtime & dependencies installed | `pip list -r requirements-prod.txt` | Prepared |
| **Settings** | Hardened production settings (`settings_production.py`) | `DEBUG = False`, `SECRET_KEY` validated | Verified |
| **Reverse Proxy** | Nginx configured with SSL, rate limits, and gzip | `nginx -t` validation passed | Prepared |
| **Database** | PostgreSQL 18 cluster operational | Connection test passed via `SELECT 1` | Verified |
| **Database** | All 11 domain migrations applied | `python manage.py showmigrations` shows `[X]` | Verified |
| **Database** | Verified Olamide discography catalogue seeded | 5 albums, 30 tracks, 6 milestones seeded | Verified |
| **Static Files** | Assets collected and hashed via WhiteNoise | `python manage.py collectstatic --noinput` | Verified (183 files) |
| **Media Storage** | `/media/` folder permissions & 5MB cap enforced | Tested upload validation & Nginx config | Verified |
| **Backups** | Automated daily dump script and cron scheduled | `scripts/backup_production.sh` verified | Prepared |
| **Health Check** | Real-time health endpoint responding | `GET /api/v1/health/` returns HTTP 200 OK | Verified |
| **Automated Tests**| Full test suite passing against PostgreSQL | 54/54 automated tests passing (0 failures) | Verified |

---

## 3. Legal, Licensing & Brand Compliance Checklist

| Item | Requirement | Verification Method | Status |
|---|---|---|---|
| **Independence Disclaimer** | Prominent disclaimer that JustBaddo is an independent fan community and NOT an official Olamide platform | Displayed in page footers, about page, and API platform metadata | **COMPLIANT** |
| **Non-Affiliation Notice** | Explicit statement: *Not affiliated with or endorsed by Olamide, YBNL Nation, or EMPIRE Distribution* | Verified in `core.context_processors` and `platform/` endpoint | **COMPLIANT** |
| **Terms of Service** | Publicly accessible Terms of Service document | Active on `/pages/terms.html` | **COMPLIANT** |
| **Privacy Policy** | Publicly accessible Privacy Policy detailing cookie and account data usage | Active on `/pages/privacy.html` | **COMPLIANT** |
| **Community Guidelines**| Published code of conduct for fan arena, discussions, and story submissions | Active on `/pages/community-guidelines.html` | **COMPLIANT** |
| **Copyright & Takedown** | Clear DMCA/copyright inquiry desk for rightsholders and representatives | Active on `/api/v1/licensing/inquiry/` and `/pages/about.html` | **COMPLIANT** |
| **Zero Unauthorized Audio**| Absolute prohibition on hosting or distributing raw MP3/AAC/FLAC audio files | Verified: No copyrighted audio binaries in codebase or database | **COMPLIANT** |
| **Playback Protection**| Tracks without verified streaming rights are locked to `METADATA_ONLY` or synthetic demo | Enforced by `PlaybackCheckView` and `MockAudioProvider` | **COMPLIANT** |

---

## 4. Outstanding Pre-Launch Blockers (Pre-Requisites for Public Traffic)

The following items represent operational prerequisites that must be executed by project management prior to flipping public DNS:

| Blocker ID | Description | Impact | Action Required | Status |
|---|---|---|---|---|
| **BLK-001** | **Domain Registration & DNS Delegation** | Users cannot reach platform without custom domain. | Purchase `justbaddo.com` (or target domain) and configure Cloudflare A records to production VPS IP. | **PENDING APPROVAL** |
| **BLK-002** | **Production Cloud Host Provisioning** | Infrastructure code is ready, but live server has not been purchased. | Authorize and provision Hetzner CPX21 ($9/mo) or DigitalOcean Droplet ($24/mo). | **PENDING APPROVAL** |
| **BLK-003** | **Production SMTP Email Gateway** | Password reset emails currently output to console in development. | Register SendGrid / AWS SES account and inject `EMAIL_HOST_PASSWORD` API key into `.env.production`. | **PENDING APPROVAL** |
| **BLK-004** | **Authorised Provider API Credentials** | Public audio playback relies on synthetic Web Audio API synthesizer. | Finalize developer account credentials with SoundCloud API or YouTube Data API for embedded playback. | **PENDING APPROVAL** |
| **BLK-005** | **Direct Rights Outreach (Phase 6)** | Long-term native streaming requires formal master and publishing clearances. | Initiate contact with YBNL Nation and EMPIRE distribution legal counsel (Phase 6). | **SCHEDULED FOR PHASE 6** |

---

## 5. Launch Sign-Off Decision

- [x] **Technical & Architectural Readiness:** APPROVED. All code, configuration, container recipes, and database schemas are prepared.
- [x] **Security Hardening:** APPROVED. Strict headers, rate limiting, and unprivileged execution verified.
- [x] **Legal Compliance:** APPROVED. Independent brand disclaimers, zero-copyright audio guardrails, and terms of service verified.
- [ ] **Public DNS Cutover:** PENDING. Awaiting user authorization to provision live hosting infrastructure and register target domain.
