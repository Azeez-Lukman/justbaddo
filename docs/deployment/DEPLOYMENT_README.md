# JUSTBADDO — DEPLOYMENT & LAUNCH DOCUMENTATION

## 1. Overview

This directory provides the authoritative production deployment and launch documentation for **JustBaddo** — an independent music and fan community platform dedicated to Olamide Baddo.

Having completed Phase 1 (Frontend), Phase 2 (Backend), Phase 3 (Database), and Phase 4 (Testing & Integration), Phase 5 establishes the infrastructure, configuration, security hardening, disaster recovery, and operational procedures necessary to deploy JustBaddo reliably and securely to production.

---

## 2. Deployment Philosophy

1. **Simplicity Over Over-Engineering:** Deploy a robust, containerized Django modular monolith fronted by Nginx and backed by PostgreSQL 18. Avoid premature microservices, Kubernetes clusters, or multi-region complexity.
2. **Strict Legal & Music Rights Compliance:** Respect all copyright boundaries. No unauthorized audio files are hosted or streamed. Audio delivery strictly uses the provider-independent abstraction layer with authorized embeds (SoundCloud / YouTube) or zero-copyright harmonic pulses.
3. **Defense in Depth:** Mandatory HTTPS, HSTS, secure cookies, CSRF defense, rate-limiting on authentication endpoints, unprivileged container runtime (`UID 1000`), and dedicated database roles.
4. **Verified Recoverability:** Automated backups (`pg_dump -Fc`) with SHA256 integrity verification, 14-day retention, and documented restoration procedures.
5. **Zero-Commitment Preparation:** All configurations, scripts, and deployment recipes are self-contained in the repository without incurring cloud bills or purchasing domains prematurely.

---

## 3. Documentation Suite Index

| Document | Purpose |
|---|---|
| [`docs/deployment/DEPLOYMENT_README.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/DEPLOYMENT_README.md) | Authoritative deployment hub, directory roadmap, and execution commands. |
| [`docs/deployment/PRODUCTION_ARCHITECTURE.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/PRODUCTION_ARCHITECTURE.md) | Hosting options evaluation, recommended architecture, component topologies, and cost analysis. |
| [`docs/deployment/ENVIRONMENT_CONFIGURATION.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/ENVIRONMENT_CONFIGURATION.md) | Comprehensive specification of all environment variables, secret management, and settings. |
| [`docs/deployment/SECURITY_CHECKLIST.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/SECURITY_CHECKLIST.md) | Production security audit, headers, authentication hardening, and incident response procedures. |
| [`docs/deployment/BACKUP_AND_RECOVERY.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/BACKUP_AND_RECOVERY.md) | Automated PostgreSQL backup strategies, rotation cycles, integrity checks, and restore guides. |
| [`docs/deployment/LAUNCH_CHECKLIST.md`](file:///c:/Users/USER/Documents/JustBaddo/docs/deployment/LAUNCH_CHECKLIST.md) | Pre-flight launch verification, legal compliance disclaimers, and outstanding blocker tracker. |

---

## 4. Production Artifacts & Directory Structure

```text
JustBaddo/
├── config/
│   ├── settings.py                 # Core Django development settings
│   └── settings_production.py      # Hardened production settings (DEBUG=False, HSTS, SSL)
├── deploy/
│   ├── gunicorn.conf.py            # Production Gunicorn WSGI configuration
│   ├── nginx/
│   │   ├── nginx.conf              # Master Nginx configuration (gzip, rate limits, timeouts)
│   │   └── conf.d/
│   │       └── justbaddo.conf      # Virtual host config (SSL, proxy pass, static/media aliases)
│   └── systemd/
│       ├── justbaddo.service       # Systemd service unit for Gunicorn WSGI daemon
│       └── justbaddo.socket        # Systemd socket unit for IPC communication
├── docs/deployment/               # Phase 5 Deployment Documentation Suite
├── scripts/
│   ├── backup_production.sh        # Automated PostgreSQL dump with SHA256 checksum & prune
│   ├── restore_production.sh       # Verified restoration script with integrity check
│   └── deploy.sh                   # Zero-downtime deployment script (pull, migrate, collect, reload)
├── .env.production.example         # Production environment variables template
├── Dockerfile                      # Multi-stage production container image (non-root runtime)
├── docker-compose.prod.yml         # Production multi-container composition (db, web, nginx, certbot)
├── requirements.txt                # Baseline application dependencies
└── requirements-prod.txt           # Production server dependencies (Gunicorn, WhiteNoise, Redis)
```

---

## 5. Deployment Quickstart

### Option A: Docker Compose Deployment (Recommended)

1. **Clone repository on production host:**
   ```bash
   git clone https://github.com/your-org/JustBaddo.git /var/www/justbaddo
   cd /var/www/justbaddo
   ```
2. **Prepare production environment file:**
   ```bash
   cp .env.production.example .env.production
   # Populate DJANGO_SECRET_KEY, POSTGRES_PASSWORD, and DJANGO_ALLOWED_HOSTS
   chmod 600 .env.production
   ```
3. **Build and launch containers:**
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```
4. **Execute database migrations and seed discography:**
   ```bash
   docker compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput
   docker compose -f docker-compose.prod.yml exec web python manage.py seed_catalogue
   ```
5. **Verify health check:**
   ```bash
   curl -I http://localhost/api/v1/health/
   ```

### Option B: Native Linux VPS (Ubuntu 24.04 LTS / Systemd)

1. **Install system packages:**
   ```bash
   sudo apt update && sudo apt install -y python3-venv python3-pip postgresql nginx certbot python3-certbot-nginx
   ```
2. **Configure PostgreSQL:**
   ```bash
   sudo -u postgres psql -c "CREATE DATABASE justbaddo_db;"
   sudo -u postgres psql -c "CREATE USER justbaddo_app_user WITH PASSWORD 'strong_password';"
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE justbaddo_db TO justbaddo_app_user;"
   ```
3. **Install application dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-prod.txt
   ```
4. **Collect static assets and run migrations:**
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings_production
   python manage.py collectstatic --noinput
   python manage.py migrate --noinput
   python manage.py seed_catalogue
   ```
5. **Enable Systemd and Nginx:**
   ```bash
   sudo cp deploy/systemd/justbaddo.service /etc/systemd/system/
   sudo cp deploy/systemd/justbaddo.socket /etc/systemd/system/
   sudo cp deploy/nginx/conf.d/justbaddo.conf /etc/nginx/conf.d/
   sudo systemctl daemon-reload
   sudo systemctl enable --now justbaddo.socket
   sudo systemctl restart nginx
   ```
