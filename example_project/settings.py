import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_DIR = os.path.dirname(__file__)

ADMINS = (
    ('Test', 'test@example.com'),
)

MANAGERS = ADMINS
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_DIR, 'kong_db')

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'
SECRET_KEY = 'BZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'kong.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.humanize',
    'kong',
)


KONG_RUN_ONLINE_TESTS = True
KONG_MAIL_ADMINS = True
KONG_MAIL_ON_EVERY_FAILURE = True

#Have local changes?
try:
    from local_settings import *
except:
    pass
