"""
Django settings for konkan_guide project.
Production-ready Render + Supabase configuration
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# ------------------------------------------------------------------------------
# BASE DIRECTORY
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / '.env')

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------

IS_PRODUCTION = os.environ.get('RENDER') == 'true' or bool(os.getenv('RENDER_EXTERNAL_HOSTNAME')) or os.environ.get('ENVIRONMENT') == 'production'

DEBUG = os.environ.get('DEBUG', 'False' if IS_PRODUCTION else 'True').lower() in ('true', '1', 'yes')

SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if not IS_PRODUCTION or DEBUG:
        SECRET_KEY = 'django-insecure-change-this-in-production-dev-only'
    else:
        raise ImproperlyConfigured("The SECRET_KEY environment variable must be set when DEBUG is False in production.")


_env_allowed_hosts = os.environ.get('ALLOWED_HOSTS')
if _env_allowed_hosts:
    ALLOWED_HOSTS = [h.strip() for h in _env_allowed_hosts.split(',') if h.strip()]
elif DEBUG:
    ALLOWED_HOSTS = [
        'konkan.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1',
        'testserver',
        '*',
    ]
else:
    ALLOWED_HOSTS = [
        'konkan.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1',
    ]

if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    render_host = os.getenv('RENDER_EXTERNAL_HOSTNAME')
    if render_host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_host)

_env_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS')
if _env_csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _env_csrf.split(',') if o.strip()]
else:
    CSRF_TRUSTED_ORIGINS = [
        'https://konkan.onrender.com',
        'https://*.onrender.com',
        'http://localhost',
        'http://127.0.0.1',
    ]

if os.getenv('RENDER_EXTERNAL_HOSTNAME'):
    render_origin = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

# ------------------------------------------------------------------------------
# PRODUCTION SECURITY & REVERSE PROXY HEADERS
# ------------------------------------------------------------------------------

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'

    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'True') == 'True'
    CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'True') == 'True'

    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'cloudinary_storage',
    'cloudinary',
    'rest_framework',
    'django_filters',

    # Local apps
    'core',
    'destinations',
    'reviews',
    'accounts',
    'spots',
    'food',
    'users',
    'companion',
    'ops',
]

# ------------------------------------------------------------------------------
# REST FRAMEWORK
# ------------------------------------------------------------------------------

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_PAGINATION_CLASS': 'config.pagination.StandardPagination',

    'PAGE_SIZE': 10,

    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    },

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ------------------------------------------------------------------------------
# MIDDLEWARE
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ------------------------------------------------------------------------------
# URLS / WSGI
# ------------------------------------------------------------------------------

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        'DIRS': [BASE_DIR / 'templates'],

        'APP_DIRS': True,

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ------------------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------------------

DATABASE_URL = os.environ.get('DATABASE_URL')

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
elif DATABASE_URL:
    db_ssl_require = os.environ.get('DB_SSL_REQUIRE', '').lower() == 'true' or 'sslmode=require' in DATABASE_URL.lower()
    db_config = dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=int(os.environ.get('DB_CONN_MAX_AGE', 600)),
        ssl_require=db_ssl_require
    )
    db_config['CONN_HEALTH_CHECKS'] = True
    DATABASES = {
        'default': db_config
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ------------------------------------------------------------------------------
# PASSWORD VALIDATION
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ------------------------------------------------------------------------------
# STATIC FILES
# ------------------------------------------------------------------------------

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# ------------------------------------------------------------------------------
# MEDIA FILES
# ------------------------------------------------------------------------------
# MEDIA FILES
# ------------------------------------------------------------------------------

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
os.makedirs(MEDIA_ROOT, exist_ok=True)

# ------------------------------------------------------------------------------
# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------

_cloudinary_cloud_name = os.environ.get('CLOUDINARY_CLOUD_NAME', '').strip()
_cloudinary_api_key = os.environ.get('CLOUDINARY_API_KEY', '').strip()
_cloudinary_api_secret = os.environ.get('CLOUDINARY_API_SECRET', '').strip()
_cloudinary_url = os.environ.get('CLOUDINARY_URL', '').strip()

if _cloudinary_url and not (_cloudinary_cloud_name and _cloudinary_api_key and _cloudinary_api_secret):
    import re
    _match = re.match(r'cloudinary:\/\/([^:]+):([^@]+)@(.+)', _cloudinary_url)
    if _match:
        _cloudinary_api_key = _match.group(1)
        _cloudinary_api_secret = _match.group(2)
        _cloudinary_cloud_name = _match.group(3)

_has_cloudinary = bool(_cloudinary_url or (_cloudinary_cloud_name and _cloudinary_api_key and _cloudinary_api_secret))

if _has_cloudinary:
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': _cloudinary_cloud_name,
        'API_KEY': _cloudinary_api_key,
        'API_SECRET': _cloudinary_api_secret,
    }
    DEFAULT_STORAGE_BACKEND = "cloudinary_storage.storage.MediaCloudinaryStorage"
else:
    DEFAULT_STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"

WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_MAX_AGE = 31536000 if not DEBUG else 0

STORAGES = {
    "default": {
        "BACKEND": DEFAULT_STORAGE_BACKEND,
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage" if DEBUG else "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ------------------------------------------------------------------------------
# DEFAULT PRIMARY KEY
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------------------------------------------------------------------------------
# AUTH REDIRECTS
# ------------------------------------------------------------------------------

LOGIN_REDIRECT_URL = 'home'

LOGOUT_REDIRECT_URL = 'login'

LOGIN_URL = 'login'
# ------------------------------------------------------------------------------
# CACHING (In-Memory Fast Cache for Static Datasets & Telemetry)
# ------------------------------------------------------------------------------

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'konkan-memory-cache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        }
    }
}
