from main.settings.local import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'fn_portal',
        'USER': 'cottrillad',
        'PASSWORD': 'django',
    }
}
