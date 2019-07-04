from main.settings.base import *

ALLOWED_HOSTS = ['*']
SECRET_KEY = 'top_secret'

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fn_portal',
        'USER': 'cottrillad',
        'PASSWORD': 'django123',
    }
}

INTERNAL_IPS = ('127.0.0.1', )

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]


INSTALLED_APPS += (
    'debug_toolbar',
    #'django_extensions',
)
