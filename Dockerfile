# ==============================================================================
# JustBaddo - Production Container Image
# Multi-stage secure build with unprivileged runtime user
# ==============================================================================

# Stage 1: Build & Dependencies
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /install

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-prod.txt ./
RUN pip install --prefix=/install/deps -r requirements-prod.txt

# Stage 2: Runtime Container
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DJANGO_SETTINGS_MODULE=config.settings_production

# Install runtime library dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create unprivileged system user and group
RUN groupadd -g 1000 justbaddo && \
    useradd -u 1000 -g justbaddo -s /bin/bash -m justbaddo

# Copy installed Python packages from builder
COPY --from=builder /install/deps /usr/local

WORKDIR /app

# Copy application source code
COPY --chown=justbaddo:justbaddo . /app

# Prepare storage directories with appropriate permissions
RUN mkdir -p /app/staticfiles /app/media /app/logs && \
    chown -R justbaddo:justbaddo /app/staticfiles /app/media /app/logs

# Switch to unprivileged runtime user
USER justbaddo

# Healthcheck testing backend readiness and database connectivity
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/api/v1/health/ || exit 1

EXPOSE 8000

# Entrypoint runs Gunicorn WSGI server
CMD ["gunicorn", "config.wsgi:application", "--config", "deploy/gunicorn.conf.py"]
