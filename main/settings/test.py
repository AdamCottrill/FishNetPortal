# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""

from main.settings.base import *

import os

# GEOS_LIBRARY_PATH = "c:/OSGeo4W/bin/geos_c.dll"
# GDAL_LIBRARY_PATH = "C:/OSGeo4W/bin/gdal300.dll"

OSGEO_VENV = "C:/1work/.virtualenv/fn_portal/Lib/site-packages/osgeo"
GEOS_LIBRARY_PATH = os.path.join(OSGEO_VENV, "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join(OSGEO_VENV, "gdal300.dll")
os.environ["PATH"] += os.pathsep + str(OSGEO_VENV)

# import os
# import pickle

# vars = {}
# for key, value in os.environ.items():
#     vars[key] = value

# pickle.dump(vars, open("vars.py", "wb"))


import sys

print("Using main.settngs.test....")
print("sys.path={}".format(sys.path))


SECRET_KEY = "testing"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "fn_portal",
        "USER": "cottrillad",
        "PASSWORD": get_env_variable("PGPASS"),
        "HOST": "localhost",
    }
}


PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


COVERAGE_MODULE_EXCLUDES = ["migrations", "fixtures", "admin$", "utils", "config"]
COVERAGE_MODULE_EXCLUDES += THIRD_PARTY_APPS + DJANGO_APPS
# COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(__file__, '../../../coverage')
#
