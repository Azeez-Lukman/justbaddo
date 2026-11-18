# JUSTBADDO — PRODUCTION SECURITY CHECKLIST

## 1. Security Overview

JustBaddo handles user authentication, session data, fan interactions, and curated discography metadata. Maintaining the confidentiality, integrity, and availability of user data is paramount.

This checklist establishes mandatory security standards that must be verified before the platform is exposed to public internet traffic.

---

## 2. Pre-Deployment Verification Matrix

| Domain | Security Requirement | Implementation / Setting | Verification Command / Status |
|---|---|---|---|
| **Django Core** | `DEBUG` mode disabled | `DEBUG = False` in `settings_production.py` | Verified in test suite & config |
| **Django Core** | Cryptographic Secret Key | 64-char random string in `DJANGO_SECRET_KEY` | Must generate via `secrets.token_urlsafe` |
| **Django Core** | Host Header Poisoning Defense | `ALLOWED_HOSTS = ['justbaddo.com', 'www.justbaddo.com']` | Disallows wildcard `*` in production |
| **Transport** | SSL/TLS Redirection | `SECURE_SSL_REDIRECT = True` | Plain HTTP returns 301 to HTTPS |
| **Transport** | HSTS Header | `SECURE_HSTS_SECONDS = 31536000`, `includeSubDomains`, `preload` | Injects Strict-Transport-Security header |
| **Transport** | Secure Cookies | `SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True` | Cookies only transmitted over HTTPS |
| **Transport** | Cookie Tampering Prevention | `SESSION_COOKIE_HTTPONLY = True`, `CSRF_COOKIE_HTTPONLY = False` | Session cookie hidden from JavaScript |
| **Browser Defenses** | Clickjacking Defense | `X_FRAME_OPTIONS = 'DENY'` | Prevents embedding in malicious iframes |
| **Browser Defenses** | MIME Sniffing Defense | `SECURE_CONTENT_TYPE_NOSNIFF = True` | Enforces declared Content-Type header |
| **Reverse Proxy** | Server Signature Hiding | `server_tokens off;` in Nginx | Hides Nginx version from response headers |
| **Reverse Proxy** | Maximum Upload Limit | `client_max_body_size 5M;` in Nginx | Rejects uploads larger than 5 Megabytes |
| **Reverse Proxy** | Brute Force Rate Limiting | `limit_req zone=auth_limit burst=5 nodelay;` | Restricts login/register to 5 req/minute |
| **API Security** | DRF Request Throttling | Anonymous: 120/min; Authenticated: 600/min | Handled via DRF throttle classes |
| **Database** | Principle of Least Privilege | Dedicated role `justbaddo_app_user` (no SUPERUSER) | PostgreSQL role grants |
| **Database** | Network Isolation | Port 5432 bound to `127.0.0.1` or internal Docker network | Blocked from public internet WAN |
| **File Storage** | Upload Validation | Extension whitelist (`.jpg`, `.jpeg`, `.png`, `.webp`) | Validated at serializer & model layer |
| **OS / Runtime** | Container Isolation | Unprivileged user `justbaddo` (UID 1000) | Non-root runtime in Dockerfile |

---

## 3. Automated Security Verification

Before deploying, run Django's built-in deployment security verification tool on the production server:

```bash
export DJANGO_SETTINGS_MODULE=config.settings_production
python manage.py check --deploy
```

### Expected Output
```text
System check identified no issues (0 silenced).
```

If any `security.W...` warnings are triggered, resolve them before pointing live public DNS records.

---

## 4. Reverse Proxy Hardening (Nginx)

1. **Modern TLS Configuration:**
   Only enable TLS 1.2 and TLS 1.3. Explicitly disable legacy and vulnerable protocols (SSLv2, SSLv3, TLS 1.0, TLS 1.1):
   ```nginx
   ssl_protocols TLSv1.2 TLSv1.3;
   ssl_prefer_server_ciphers on;
   ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
   ```

2. **Rate Limiting Zones:**
   Prevent credential stuffing and denial of service:
   ```nginx
   limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
   limit_req_zone $binary_remote_addr zone=api_general:10m rate=20r/s;
   ```

3. **Restricting Media Execution:**
   Ensure user-uploaded media files cannot be executed as server-side scripts:
   ```nginx
   location /media/ {
       alias /var/www/justbaddo/media/;
       expires 7d;
       add_header Cache-Control "public, max-age=604800";
       # Disable script execution
       types {
           image/jpeg jpg jpeg;
           image/png png;
           image/webp webp;
           image/gif gif;
       }
       default_type application/octet-stream;
   }
   ```

---

## 5. Security Incident Response Procedure

In the event of a suspected security incident, credential breach, or anomalous activity:

### Step 1: Triage and Containment
1. If an active exploit is detected, temporarily take the public site into maintenance mode:
   ```bash
   sudo systemctl stop nginx
   ```
2. Isolate network access to the server via cloud firewall (allow SSH from administrator IP only).

### Step 2: Credential & Secret Invalidation
1. Invalidate all user sessions and CSRF tokens by rotating `DJANGO_SECRET_KEY` in `.env.production`.
2. Rotate the PostgreSQL database user password:
   ```sql
   ALTER USER justbaddo_app_user WITH PASSWORD 'new_strong_password_string';
   ```
3. Update `POSTGRES_PASSWORD` in `.env.production`.

### Step 3: Forensic Log Analysis
Inspect application and security logs for unauthorized traversal or privilege escalation:
- `/var/www/justbaddo/logs/justbaddo_security.log`
- `/var/www/justbaddo/logs/justbaddo_app.log`
- `/var/log/nginx/access.log` and `/var/log/nginx/error.log`

### Step 4: System Restoration and Verification
1. Run `python manage.py test` to ensure system integrity.
2. Restart application services:
   ```bash
   sudo systemctl start justbaddo.service
   sudo systemctl start nginx
   ```
3. Monitor real-time logs and verify normal operations via `/api/v1/health/`.
