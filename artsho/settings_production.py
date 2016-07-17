# flake8: noqa
from settings_shared import *
import os

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
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

INSTALLED_APPS += [
    'opbeat.contrib.django',
]
MIDDLEWARE_CLASSES.insert(0, 'opbeat.contrib.django.middleware.OpbeatAPMMiddleware')

AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', '')
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY', '')
AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = AWS_SECRET_KEY

if AWS_S3_CUSTOM_DOMAIN:
    AWS_PRELOAD_METADATA = True
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'https://%s/' % AWS_S3_CUSTOM_DOMAIN
    # static data, e.g. css, js, etc.
    STATICFILES_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'
    STATIC_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
    COMPRESS_ENABLED = True
    COMPRESS_OFFLINE = True
    COMPRESS_ROOT = STATIC_ROOT
    COMPRESS_URL = STATIC_URL
    COMPRESS_STORAGE = 'cacheds3storage.CompressorS3BotoStorage'

try:
    from local_settings import *
except ImportError:
    pass
