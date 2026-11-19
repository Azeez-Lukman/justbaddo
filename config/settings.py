"""
Django settings for JustBaddo project (Phase 2: Backend Development).

Modular Django Monolith configured for REST APIs and template rendering.
Prepared with environment-driven PostgreSQL configuration for Phase 3.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-ld_dpon5@#aja^j%9wiptllwfn4fr0b#^^rw2wtr5zczzp$g!l'
)

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = os.environ.get(
    'DJANGO_ALLOWED_HOSTS',
    'localhost 127.0.0.1 [::1] *'
).split()

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'corsheaders',
]

JUSTBADDO_APPS = [
    'core.apps.CoreConfig',
    'accounts.apps.AccountsConfig',
    'music.apps.MusicConfig',
    'playback.apps.PlaybackConfig',
    'playlists.apps.PlaylistsConfig',
    'community.apps.CommunityConfig',
    'arena.apps.ArenaConfig',
    'stories.apps.StoriesConfig',
    'notifications.apps.NotificationsConfig',
    'licensing.apps.LicensingConfig',
    'moderation.apps.ModerationConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + JUSTBADDO_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'frontend',
            BASE_DIR / 'frontend' / 'pages',
            BASE_DIR / 'frontend' / 'components',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database Configuration (Environment-driven for PostgreSQL / SQLite Dev Fallback)
# In Phase 2, supports SQLite development fallback while preparing full PostgreSQL specs for Phase 3.
DB_ENGINE = os.environ.get('DJANGO_DB_ENGINE', '')
if os.environ.get('DATABASE_URL'):
    import urllib.parse
    db_url = urllib.parse.urlparse(os.environ['DATABASE_URL'])
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_url.path.lstrip('/'),
            'USER': db_url.username or 'postgres',
            'PASSWORD': urllib.parse.unquote(db_url.password or ''),
            'HOST': db_url.hostname or 'localhost',
            'PORT': db_url.port or 5432,
            'CONN_MAX_AGE': 600,
        }
    }
elif DB_ENGINE == 'postgresql' or 'POSTGRES_DB' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'justbaddo_db'),
            'USER': os.environ.get('POSTGRES_USER', 'postgres'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', ''),
            'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
            'PORT': os.environ.get('POSTGRES_PORT', '5432'),
            'CONN_MAX_AGE': 600,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend' / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media Files (User avatars, submission attachments)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
MAX_UPLOAD_SIZE_BYTES = 5 * 1024 * 1024  # 5MB limit
ALLOWED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Django REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '120/min',
        'user': '600/min',
        'auth_attempt': '5/min',
    },
}

# CORS Configuration
CORS_ALLOW_ALL_ORIGINS = DEBUG
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://localhost:5500',
]
CORS_ALLOW_CREDENTIALS = True

# CSRF & Security
CSRF_COOKIE_HTTPONLY = False  # Allows frontend JavaScript to read CSRF token
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:3000',
]

# Email settings
MAILERS = {
    'default': {
        'BACKEND': 'django.core.mail.backends.console.EmailBackend',
    },
}

# Platform Brand & Licensing Declarations
JUSTBADDO_PLATFORM_NAME = 'JustBaddo'
JUSTBADDO_AFFILIATION_DISCLAIMER = (
    'JustBaddo is an independent fan community platform dedicated to Olamide Baddo. '
    'It is not officially affiliated with or endorsed by Olamide, YBNL Nation, or Empire Distribution.'
)
