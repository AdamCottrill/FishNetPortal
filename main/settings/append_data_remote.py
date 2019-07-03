from main.settings.base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '142.143.160.56',
        'NAME': 'fn_portal',
        'USER': 'cottrillad',
        'PASSWORD': 'django123',
    }
}
