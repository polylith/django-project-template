import logging
import os
import sys
from _socket import gethostname, gethostbyname

SERVICE_NAME = "@= project_name =@"

production = bool(os.getenv('PRODUCTION', False))
DEBUG = True if not production else False
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration

sentry_logging = LoggingIntegration(
    level=logging.DEBUG,
    event_level=logging.ERROR
)

if not DEBUG:
    sentry_sdk.init(
        dsn="CHANGE_ME",
        environment=os.getenv('ENVIRONMENT', 'local'),
        integrations=[sentry_logging, DjangoIntegration()]
    )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s|%(asctime)s|%(name)s>> %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

SECRET_KEY = "6e2bmahu38vuzy0fd2xw*jz32*9tva_lp=$c!^v6pu)-4qd4k7"

EXPOSED_DOMAIN = f'@= project_name =@.{os.getenv("ENVIRONMENT_DOMAIN", "")}'

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "@= project_name =@",
    "@= project_name =@.default",
    gethostname(),
    gethostbyname(gethostname()),
    EXPOSED_DOMAIN,
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "commands",
    "django_prometheus",
    "events",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "cors.CORSMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


TEST_RUNNER = "teamcity.django.TeamcityDjangoRunner"

import dj_database_url
import docker_database_url

default_database_url = os.getenv(
    "DATABASE_URL",
    docker_database_url.start_db_and_get_url(
        db_name="@= project_name =@_db", database_url_name="DATABASE_URL"
    ),
)
events_database_url = os.getenv(
    "EVENTS_DATABASE_URL",
    docker_database_url.start_db_and_get_url(
        db_name="events_db", database_url_name="EVENTS_DATABASE_URL"
    ),
)

DATABASES = {
    "default": dj_database_url.parse(default_database_url),
    "events_db": dj_database_url.parse(events_database_url),
}

DATABASE_ROUTERS = ["events.router.Router"]


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_URL = "/media/"

if DEBUG:
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    MEDIA_ROOT = "media"
    if os.getenv("MEDIA_S3_BUCKET_NAME") is None:
        error = "MEDIA_S3_BUCKET_NAME is not set!"
        raise RuntimeError(error)
    if os.getenv("MEDIA_S3_REGION_NAME") is None:
        error = "MEDIA_S3_REGION_NAME is not set!"
        raise RuntimeError(error)

    AWS_ACCESS_KEY_ID = None
    AWS_SECRET_ACCESS_KEY = None
    AWS_STORAGE_BUCKET_NAME = os.getenv("MEDIA_S3_BUCKET_NAME")
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    AWS_S3_REGION_NAME = os.getenv("MEDIA_S3_REGION_NAME")
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("CACHE_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "@= project_name_with_underscore =@_",
    }
}
if DEBUG and not os.getenv("CACHE_URL", None):
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
            "LOCATION": "database_cache",
        }
    }


PROMETHEUS_EXPORT_MIGRATIONS = False

DISABLE_SERVER_SIDE_CURSORS = True

REGISTERED_EVENTS = {}
EVENTS_THAT_GETS_GENERATED_BY_THIS_SERVICE = []