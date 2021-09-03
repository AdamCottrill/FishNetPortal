import os

from main.settings.base import *

DEBUG = True

print("using c:/1work/fsdviz/config/settings/local.py")

# install gdal in virtualenv:
VIRTUAL_ENV = os.environ["VIRTUAL_ENV"]
OSGEO_VENV = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo")
GEOS_LIBRARY_PATH = os.path.join(OSGEO_VENV, "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join(OSGEO_VENV, "gdal302.dll")
PROJ_LIB = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/proj")

os.environ["GDAL_DATA"] = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/gdal")
os.environ["PROJ_LIB"] = PROJ_LIB
os.environ["PATH"] += os.pathsep + str(OSGEO_VENV)

geolibs = [
    ("OSGEO_VENV", OSGEO_VENV),
    ("GEOS_LIBRARY_PATH", GEOS_LIBRARY_PATH),
    ("GDAL_LIBRARY_PATH", GDAL_LIBRARY_PATH),
    ("PROJ_LIB", PROJ_LIB),
]

for lib in geolibs:
    if not os.path.exists(lib[1]):
        print("Unable to find {} at {}".format(*lib))

# # SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "*"]

INTERNAL_IPS = ("127.0.0.1",)
MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
INSTALLED_APPS += ["debug_toolbar", "django_extensions"]


SECRET_KEY = get_env_variable("SECRET_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "NAME": "fn_portal",
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
