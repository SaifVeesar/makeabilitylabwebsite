"""
Django settings for makeabilitylab project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from configparser import ConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load a ConfigParser object from a file called config.ini at the base level
# of the django project.
config = ConfigParser()
config.read(os.path.join(BASE_DIR, 'config.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if config.has_option('Django', 'SECRET_KEY'):
    SECRET_KEY = config.get('Django', 'SECRET_KEY')
else:
    # We should never be in production with this key
    SECRET_KEY = 'pe)-#st8rk!pomy!_1ha7=cpypp_(8%1xqmtw%!u@kw-f5&w^e' 

# SECURITY WARNING: don't run with debug turned on in production!
#  we will default to True if not overriden in the config file
if config.has_option('Django', 'DEBUG'):
    DEBUG = config.getboolean('Django', 'DEBUG')
else:
    DEBUG = True

# TODO: Take this out when done debugging production
# DEBUG = True

if config.has_option('Django', 'ALLOWED_HOSTS'):
    USE_X_FORWARDED_HOST = True
    ALLOWED_HOSTS = config.get('Django', 'ALLOWED_HOSTS').split(',')
else:
    ALLOWED_HOSTS = []


# TODO: this seems to work fine on Docker but breaks localhost dev (without docker)
# See: https://docs.djangoproject.com/en/2.0/topics/logging/
# https://lincolnloop.com/blog/django-logging-right-way/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/code/media/debug.log',
            'maxBytes': 1024*1024*10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',  # can switch between verbose and simple
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'website': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# Application definition

INSTALLED_APPS = [
    'website.apps.WebsiteConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # To use IPython-enabled Django shell through Django extensions
    # pip3 install django_extensions
    # python manage.py shell_plus
    # https://opensourcehacker.com/2014/08/13/turbocharge-your-python-prompt-and-django-shell-with-ipython-notebook/
    'django_extensions',
    'image_cropping',
    'easy_thumbnails',
    'sortedm2m',
    'sortedm2m_filter_horizontal_widget',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'makeabilitylab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.recent_news'
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
if ALLOWED_HOSTS:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config.get('Postgres', 'DATABASE'),
            'USER': config.get('Postgres', 'USER'),
            'PASSWORD': config.get('Postgres', 'PASSWORD'),
            'HOST': config.get('Postgres', 'HOSTNAME'),
            'PORT': '',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db', 'db.sqlite3'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Change timezone for server: https://stackoverflow.com/questions/29311354/how-to-set-the-timezone-in-django
TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# JEF: I added these for uploading files.
# See:
#   http://stackoverflow.com/questions/22570723/handling-uploading-image-django-admin-python
#   https://github.com/axelpale/minimal-django-file-upload-example
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Thumbnail processing
# LS: from https://github.com/jonasundderwolf/django-image-cropping
from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
