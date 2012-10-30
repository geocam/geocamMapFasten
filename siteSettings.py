# __BEGIN_LICENSE__
# Copyright (C) 2008-2010 United States Government as represented by
# the Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# __END_LICENSE__

# siteSettings.py -- site default settings
#
# This contains the default settings for the site-level django app.  This will
# override any application-default settings and define the default set of
# installed applications. This should be a full settings.py file which needs
# minimal overrides by the settings.py file for the application to actually
# function.
#
# As a bare minimum, please edit INSTALLED_APPS!
#
# This file *should* be checked into git.

from django.conf import global_settings

DEBUG = True
TEMPLATE_DEBUG = DEBUG
import os
import sys
#APP = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJ_ROOT = os.path.abspath(os.path.dirname(__file__))

PIPELINE_YUI_BINARY = "/usr/bin/yui-compressor"

SCRIPT_NAME = os.environ['DJANGO_SCRIPT_NAME']  # set in sourceme.sh
USING_DJANGO_DEV_SERVER = ('runserver' in sys.argv)
if USING_DJANGO_DEV_SERVER:
    # django dev server deployment won't work with other SCRIPT_NAME settings
    SCRIPT_NAME = '/'

USE_STATIC_SERVE = USING_DJANGO_DEV_SERVER

# Python path is agnostic to what the site-level dir is. It also prefers the
# checked-out version of an app over the standard python install locations.
sys.path.append(PROJ_ROOT)

ADMINS = (
    # ('mfsmith3', 'your_email@domain.com'),
)
MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT  = os.path.join(PROJ_ROOT, "data", "")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = SCRIPT_NAME + "data/"

# Absolute path to the directory that holds data. This is different than media
# in that it's uploaded/processed data that's not needed for the operation of
# the site, but may need to be network-accessible, or be linked to from the
# database. Examples: images, generate kml files, etc.
# Example: "/data/"
DATA_ROOT = os.path.join(PROJ_ROOT, "data", "")

DATA_DIR = DATA_ROOT  # some legacy modules use the DATA_DIR name

# URL that handles the data served from DATA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://data.lawrence.com", "http://example.com/data/"
DATA_URL = SCRIPT_NAME + "data/"

STATIC_ROOT = os.path.join(PROJ_ROOT, "build", "static", "")
STATIC_URL = SCRIPT_NAME + 'static/'

# helper for django-pipeline
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Awesome. Needed in Django 1.3 but causes deprecation warning in Django 1.4.
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = global_settings.TEMPLATE_LOADERS + (
#)

MIDDLEWARE_CLASSES = (
    'geocamUtil.middleware.LogErrorsMiddleware',
) + global_settings.MIDDLEWARE_CLASSES + (
    'django.middleware.gzip.GZipMiddleware',
    'geocamUtil.middleware.SecurityMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# Note: the order of INSTALLED_APPS affects the search order for
# templates.  We suggest putting your apps above standard apps
# so your apps can override templates as needed.
INSTALLED_APPS = (
    'mapFastenApp',
    'geocamTiePoint',

    'geocamUtil',

    'django_digest',
    'pipeline'

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)

GEOCAM_UTIL_SECURITY_ENABLED = False  # not USING_DJANGO_DEV_SERVER
GEOCAM_UTIL_SECURITY_SSL_REQUIRED_BY_DEFAULT = False
GEOCAM_UTIL_SECURITY_REQUIRE_ENCRYPTED_PASSWORDS = False
GEOCAM_UTIL_SECURITY_LOGIN_REQUIRED_BY_DEFAULT = 'write'
GEOCAM_UTIL_SECURITY_ACCEPT_AUTH_TYPES = ('basic',)

# note: LOGIN_URL and LOGOUT_URL will not be respected on app engine when using
# google's integrated auth system. LOGIN_REDIRECT_URL is respected.
LOGIN_URL = SCRIPT_NAME + 'accounts/login/'
LOGOUT_URL = SCRIPT_NAME + 'accounts/logout/'
LOGIN_REDIRECT_URL = SCRIPT_NAME

SITE_TITLE = 'MapFasten'

GEOCAM_UTIL_INSTALLER_USE_SYMLINKS = True

USING_APP_ENGINE_DEV_SERVER = (os.getenv('SERVER_SOFTWARE', '').startswith('Development/')
                               or os.getenv('SETTINGS_MODE') == 'devappengine')
USING_APP_ENGINE_REAL = (os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine')
                         or os.getenv('SETTINGS_MODE') == 'appengine')
USING_APP_ENGINE = USING_APP_ENGINE_DEV_SERVER or USING_APP_ENGINE_REAL

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS

if USING_APP_ENGINE:
    # sqlite doesn't work in real app engine environment, use google cloud sql
    DATABASES = {
        'default': {
            'ENGINE': 'google.appengine.ext.django.backends.rdbms',
            'INSTANCE': 'mapfasten1:mapfasten', # the cloud sql "instance name"
            'NAME': 'make your own dev sandbox and overwrite this value in settings.py',
        }
    }
else:
    # use local sqlite database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJ_ROOT, 'dev.db')
        }
    }

if USING_APP_ENGINE_REAL:
    DATABASES['default']['NAME'] = 'mapfasten'

if USING_APP_ENGINE:
    DEFAULT_FILE_STORAGE = 'geocamAppEngine.storage.BlobStorage'
    MIDDLEWARE_CLASSES += (
        'geocamAppEngine.middleware.AuthenticationMiddleware',
        'mapFastenApp.middleware.ClosedBetaMiddleware',
    )
    TEMPLATE_CONTEXT_PROCESSORS += (
        'geocamAppEngine.context_processors.AuthUrlsContextProcessor',
    )

else:
    TEMPLATE_CONTEXT_PROCESSORS += (
        'geocamUtil.context_processors.AuthUrlsContextProcessor.AuthUrlsContextProcessor',
    )

# easy zero-install caching setup, fine with django dev server
SIMPLE_CACHE_ = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 0
    }
}

# real caching setup, works better in multi-process environment
MEMCACHED_CACHE_ = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 0
    }
}

CACHES = SIMPLE_CACHE_
