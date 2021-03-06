"""
Django settings for baros project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
import dj_database_url
from django.contrib.messages import constants as messages

SETTINGS_DIR = os.path.dirname(__file__)

PROJECT_PATH = os.path.abspath(os.path.join(SETTINGS_DIR, os.pardir))

#DATABASE_PATH = os.path.join(PROJECT_PATH, 'baros.db')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SJCLAB_DJANGO_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['sjclab.herokuapp.com', 'localboast.com', 'http://127.0.0.1', 'localhost']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    # 'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'inventory',
    'storages',
    's3_folder_storage',
    # 'registration',
    'gunicorn',
    #'debug_toolbar.apps.DebugToolbarConfig',
    'collectfast',
    'django_wysiwyg',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'urls'

WSGI_APPLICATION = 'baros.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = { 'default': dj_database_url.config(default="postgres://tpnouofpumqcxu:vmy3QUw4pc1NPe2J0zspFogeJQ@ec2-54-243-202-84.compute-1.amazonaws.com:5432/d8uq0t88c2k6sm") }
DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql_psycopg2'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'EST'
USE_I18N = False
USE_L10N = False
USE_TZ = True

TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')

TEMPLATE_DIRS = (
     # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
    )
    
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.static"
)

# Override bootstrap error class
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/experiments/'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# AWS S3 Storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_DIRS = ("C:/Users/Owner/Code/sjclab/static/",)
DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
DEFAULT_S3_PATH = "media"
#STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
STATICFILES_STORAGE = "storages.backends.s3boto.S3BotoStorage"
STATIC_S3_PATH = "static"
AWS_STORAGE_BUCKET_NAME = "sjclab-assets"

MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
MEDIA_URL = 'https://sjclab-assets.s3.amazonaws.com/media/'
STATIC_ROOT = "/%s/" % STATIC_S3_PATH
STATIC_URL = 'https://sjclab-assets.s3.amazonaws.com/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

AWS_PRELOAD_METADATA = True
AWS_AUTO_CREATE_BUCKET = True
#AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_IS_GZIPPED = False

# Email settings
EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
EMAIL_HOST= 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
ADMIN_EMAILS = os.environ['ADMIN_EMAILS'].split(', ')