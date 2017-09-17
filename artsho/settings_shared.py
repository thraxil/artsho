# Django settings for artsho project.
import os.path
import sys

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'artsho',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
TEST_OUTPUT_DIR = 'reports'

PROJECT_APPS = [
    'artsho.main',
    'artsho.bidauth',
]
TEST_PROJECT_APPS = [
    'artsho.main',
    'artsho.bidauth',
]

ALLOWED_HOSTS = ['localhost', '.spokehub.org', 'artsho.org', '.artsho.org']

USE_TZ = True
TIME_ZONE = 'GMT'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/artsho/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'artsho.main.contextprocessors.menu_items',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = [
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'impersonate.middleware.ImpersonateMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

ROOT_URLCONF = 'artsho.urls'

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_markwhat',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.admin',
    'compressor',
    'django_statsd',
    'bootstrap3',
    'bootstrapform',
    'waffle',
    'discover_jenkins',
    'smoketest',
    'infranil',
    'flatblocks',
    'impersonate',
    'gunicorn',
    'artsho.main',
    'artsho.bidauth',
]

INTERNAL_IPS = ('127.0.0.1', )

STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'artsho'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[artsho] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "artsho@spokehub.org"
DEFAULT_FROM_EMAIL = SERVER_EMAIL
SITE_BASE = "https://artsho.org"

STATIC_ROOT = "/tmp/artsho/static"
STATICFILES_DIRS = ["media/"]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"
COMPRESS_OFFLINE = True

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
LOGIN_REDIRECT_URL = "/"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
BIDAUTH_SECRET = 'this-gets-overridden-in-local_settings-on-production'

RETICULUM_UPLOAD_BASE = 'http://reticulum.thraxil.org/'
RETICULUM_PUBLIC_BASE = 'https://d2f33fmhbh7cs9.cloudfront.net'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
