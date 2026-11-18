# JUSTBADDO — ENVIRONMENT CONFIGURATION SPECIFICATION

## 1. Overview

JustBaddo adheres strictly to **Twelve-Factor App** principles for configuration. All environment-specific settings (database credentials, domain names, cryptographic keys, email gateways, and service endpoints) are decoupled from the codebase and injected via environment variables.

In production, these variables are loaded into the runtime process using `.env.production` (via Systemd `EnvironmentFile` or Docker Compose `env_file`).

---

## 2. Environment Variables Reference Table

| Variable Name | Type | Required? | Default / Example | Purpose & Security Implication |
|---|---|---|---|---|
| `DJANGO_SETTINGS_MODULE` | String | **Yes** | `config.settings_production` | Selects the hardened production configuration module. |
| `DJANGO_DEBUG` | Boolean | **Yes** | `False` | **Must always be `False` in production.** Setting to `True` leaks full source code, stack traces, and environment variables on error. |
| `DJANGO_SECRET_KEY` | String | **Yes** | *None* (Must generate) | Cryptographic seed used for session signing, CSRF tokens, and password reset tokens. Must be a 64+ char random string. |
| `DJANGO_ALLOWED_HOSTS` | Comma List | **Yes** | `justbaddo.com,www.justbaddo.com` | Prevents HTTP Host header poisoning attacks. Django rejects any request whose `Host` header is not listed. |
| `DJANGO_SECURE_SSL_REDIRECT`| Boolean | Optional | `True` | Automatically redirects all plain HTTP requests to HTTPS. |
| `DJANGO_HSTS_SECONDS` | Integer | Optional | `31536000` (1 Year) | Instructs browsers via HTTP Strict Transport Security to only connect via HTTPS. |
| `DJANGO_CORS_ALLOWED_ORIGINS`| Comma List | Optional | `https://justbaddo.com,https://www.justbaddo.com` | Whitelist of client origins permitted to make cross-origin requests. |
| `DJANGO_CSRF_TRUSTED_ORIGINS`| Comma List | **Yes** | `https://justbaddo.com,https://www.justbaddo.com` | Prevents cross-site request forgery by verifying origin against this whitelist. |
| `DJANGO_DB_ENGINE` | String | **Yes** | `postgresql` | Selects PostgreSQL ORM database backend. |
| `POSTGRES_DB` | String | **Yes** | `justbaddo_db` | Name of the production database. |
| `POSTGRES_USER` | String | **Yes** | `justbaddo_app_user` | Dedicated unprivileged PostgreSQL application user. |
| `POSTGRES_PASSWORD` | String | **Yes** | *None* (Must generate) | Strong password for PostgreSQL user. |
| `POSTGRES_HOST` | String | **Yes** | `db` (Docker) or `localhost` (VPS) | PostgreSQL hostname or IP address. |
| `POSTGRES_PORT` | Integer | Optional | `5432` | Standard PostgreSQL port. |
| `DB_CONN_MAX_AGE` | Integer | Optional | `600` (10 mins) | Database persistent connection lifetime in seconds. |
| `DJANGO_STATIC_ROOT` | String | Optional | `/var/www/justbaddo/staticfiles` | Absolute filesystem path where `collectstatic` outputs assets. |
| `DJANGO_MEDIA_ROOT` | String | Optional | `/var/www/justbaddo/media` | Absolute path for user uploads and assets. |
| `EMAIL_HOST` | String | Optional | `smtp.sendgrid.net` | Outgoing SMTP server hostname. |
| `EMAIL_PORT` | Integer | Optional | `587` | SMTP port (typically 587 for TLS). |
| `EMAIL_USE_TLS` | Boolean | Optional | `True` | Enforce TLS encryption for outgoing email. |
| `EMAIL_HOST_USER` | String | Optional | `apikey` | SMTP username. |
| `EMAIL_HOST_PASSWORD` | String | Optional | *SMTP API Key* | API key or password for outgoing email gateway. |
| `DEFAULT_FROM_EMAIL` | String | Optional | `JustBaddo <noreply@justbaddo.com>` | Sender address on transactional emails. |
| `GUNICORN_WORKERS` | Integer | Optional | `5` | Number of worker processes: `(2 * CPU cores) + 1`. |
| `GUNICORN_THREADS` | Integer | Optional | `4` | Number of threads per worker in `gthread` mode. |

---

## 3. Cryptographic Secret Generation

Never use default or guessable secret keys in production. Generate a cryptographically secure 64-character token on the production server using Python:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

*Example Output:*
```text
k9Fq2Z1wT8yP4vX6cR3mB0jL5eA7sD9uV2xG1nH4oJ6eW8rT0yU3iO5pA7sD9fG
```

Assign this value to `DJANGO_SECRET_KEY` in `.env.production`.

---

## 4. File Permissions and Secret Hygiene

1. **Strict File Permissions:**
   The `.env.production` file contains root secrets and database credentials. It must be accessible exclusively by the application user:
   ```bash
   chown justbaddo:justbaddo /var/www/justbaddo/.env.production
   chmod 600 /var/www/justbaddo/.env.production
   ```

2. **Git Version Control Exclusion:**
   Verify that `.env` and `.env.production` are strictly tracked by `.gitignore`:
   ```bash
   git check-ignore -v .env .env.production
   ```
   *Expected Output:*
   ```text
   .gitignore:1:.env
   .gitignore:2:.env.production
   ```

3. **Secret Rotation Procedure:**
   If a secret or credential is inadvertently exposed:
   1. Immediately update `.env.production` with a freshly generated secret.
   2. Reset database user password in PostgreSQL:
      ```sql
      ALTER USER justbaddo_app_user WITH PASSWORD 'new_strong_password';
      ```
   3. Update `POSTGRES_PASSWORD` in `.env.production`.
   4. Gracefully restart Gunicorn to invalidate all active session tokens and load the new secret:
      ```bash
      sudo systemctl restart justbaddo.service
      ```
