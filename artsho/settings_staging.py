# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/artsho/artsho/artsho/templates",
)

MEDIA_ROOT = '/var/www/artsho/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/artsho/artsho/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'artsho',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/artsho/artsho/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
STAGING_ENV = True

STATSD_PREFIX = 'artsho-staging'

try:
    from local_settings import *
except ImportError:
    pass
