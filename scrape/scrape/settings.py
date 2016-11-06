import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '2(s%qab2ha_y=h6cw%_)30nkg!)he@xl1k@!s3ar%vv$bhr*4@'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'transfer',
    'tag',
    'core',
    'blog',
    'diva',
    'char',
    'toon',
    'feeder',

    'extoon',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'scrape.urls'

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

WSGI_APPLICATION = 'scrape.wsgi.application'

DATABASE_ROUTERS = ['scrape.dbrouter.DBRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'exantenna_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
    'transfer': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'antenna_org',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
    'extoon': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'extoon_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': 5432,
    },
}

REDISES = {
    'item': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default-location'
    },
    'feed': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'feed-location',
        'TIMEOUT': 60 * 60 * 24 * 1,  # 1 days
        'KEY_FUNCTION': lambda key, key_prefix, version: key,
    },
    'tmp_image': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'tmpimage-location',
        'TIMEOUT': 60 * 60 * 24 * 5,  # 5 days
    },
    'tmp_anything': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'tmp_anything-location',
        'TIMEOUT': 60 * 60 * 1,  # 1 hours
    },
    'imginfo': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'imginfo-location',
        'TIMEOUT': 60 * 60 * 24 * 5,  # 5 days
        'KEY_FUNCTION': lambda key, key_prefix, version: key,
    },
    'lock_in_task': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'lock-in-task-cache',
        'TIMEOUT': None,
    },
}

SERVER_EMAIL = "noreply@{}".format(socket.gethostname())
DEFAULT_FROM_EMAIL = SERVER_EMAIL

EMAIL_BACKEND = 'django_mailgun.MailgunBackend'

LOGGING_PREFIX = 'scrape'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'formatters': {
        'verbose': {
            'format': ('[in %(pathname)s:%(lineno)d] '
                       '%(asctime)s %(process)d %(thread)d '
                       '%(levelname)s %(module)s: %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'syslog_verbose': {
            'format': (LOGGING_PREFIX + ': [in %(pathname)s:%(lineno)d] '
                       '%(asctime)s %(process)d %(thread)d '
                       '%(levelname)s %(module)s: %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'sql': {
            'format': '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sql'
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'verbose',
            'include_html': True,
            'email_backend': EMAIL_BACKEND,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.db.backends': {
            'handlers': ['sql'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'django.request': {
        #     'handlers': ['mail_admins'],
        #     'level': 'ERROR',
        #     'propagate': True,
        # },
        LOGGING_PREFIX: {
            'handlers': ['console', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True
        },
        'celery.task': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

USER_AGENT = {
    'chrome': (
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    ),
    'firefox': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
        'rv:49.0) Gecko/20100101 Firefox/49.0'
    ),
}

USER_AGENTS = []

ALLOW_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']

VIDEO_ELEMENTS = []

ENDPOINTS = {}

ADMINS = []
