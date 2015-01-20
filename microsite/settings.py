import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = ')c#(=l$5n+6xc7irx%7u(0)^%h##tj2d=v*_5#62m=o&zc_g7p'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

BROKER_URL = 'redis://localhost:6379/0'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'django_inbound_email',
    'micro_admin',
    'projects',
    'pages',
    'micro_blog',
    'micro_kb',
    'employee',
    'sorl.thumbnail',
    'microsite_front',
    'haystack',
    'pingback',
    'django_xmlrpc',
    'compressor',
)

import djcelery
djcelery.setup_loader()

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


ROOT_URLCONF = 'microsite.urls'

WSGI_APPLICATION = 'microsite.wsgi.application'
AUTH_USER_MODEL = 'micro_admin.User'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'micropyramid'
EMAIL_HOST_PASSWORD = 'wiej4djs3o5s'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_USER = "micropyramid"
SENDGRID_PASSWORD = "wiej4djs3o5s"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR + '/static',)

COMPRESS_ROOT=BASE_DIR + '/static/'
BLOG_IMAGES = BASE_DIR + '/static/blog/' 
TEAM_IMAGES = BASE_DIR + '/static/team/'
CLIENT_IMAGES = BASE_DIR + '/static/client/'
TRAINER_IMAGES = BASE_DIR + '/static/trainer/'
COURSE_IMAGES = BASE_DIR + '/static/course/'
QACAT_IMAGES = BASE_DIR + '/static/qacategory/'

TEMPLATE_DIRS = (BASE_DIR +'/templates',)

MEDIA_ROOT = BASE_DIR
SITE_BLOG_URL = "/blog/"

TEMPLATE_LOADERS = (
    ("django.template.loaders.cached.Loader", (
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    )),
)
COMPRESS_ENABLED=True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-30-seconds': {
        'task': 'micro_blog.tasks.scraper_example',
        'schedule':timedelta(seconds=30),
        'args': (),
    },
}

SG_USER = os.getenv('SG_USER'),
SG_PWD =  os.getenv('SG_PWD')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


from urlparse import urlparse

es = urlparse(os.environ.get('SEARCHBOX_URL') or 'http://127.0.0.1:9200/')

port = es.port or 80

# import elasticstack
# from haystack.backends.elasticsearch_backend import *

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:8983/solr',
        'INDEX_NAME': 'documents',
    },
}


if es.username:
    HAYSTACK_CONNECTIONS['default']['KWARGS'] = {"http_auth": es.username + ':' + es.password}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

DEBUG = True

ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

SITE_URL = "http://micropyramid.com"

# the fully-qualified path to the provider's backend parser
INBOUND_EMAIL_PARSER = 'django_inbound_email.backends.sendgrid.SendGridRequestParser'

# if True (default=False) then log the contents of each inbound request
INBOUND_EMAIL_LOG_REQUESTS = True

# if True (default=True) then always return HTTP status of 200 (may be required by provider)
INBOUND_EMAIL_RESPONSE_200 = True

