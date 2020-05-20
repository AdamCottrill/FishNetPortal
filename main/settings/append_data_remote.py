from main.settings.base import *


GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal204.dll"


DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": "142.143.160.56",
        "NAME": "fisheye",
        "USER": "cottrillad",
        "PASSWORD": "django",
    }
}
