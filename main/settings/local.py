from main.settings.base import *

GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal300.dll"

ALLOWED_HOSTS = ["*"]
SECRET_KEY = "top_secret"

DEBUG = True

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "fn_portal",
        "USER": "cottrillad",
        "PASSWORD": "django123",
    }
}

INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]


INSTALLED_APPS += (
    "debug_toolbar",
    #'django_extensions',
)

CORS_ORIGIN_ALLOW_ALL = True
COR_ORIGIN_WHITELIST = ("http://127.0.0.1:3000", "http://localhost:3000")
