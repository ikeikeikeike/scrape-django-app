import os

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

    'core',
    'blog',
    'diva',
    'char',
    'toon',
    'feeder',
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

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
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
        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    ),
    'firefox': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; '
        'rv:47.0) Gecko/20100101 Firefox/47.0'
    ),
}

ALLOW_EXTENSIONS = ['.jpg', '.jpeg', '.gif', '.png', '.bmp']

VIDEO_ELEMENTS = []

ENDPOINTS = {}
