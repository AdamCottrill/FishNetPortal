# usage: python manage.py test pjtk2 --settings=main.test_settings
# flake8: noqa
"""Settings to be used for running tests."""

from main.settings.base import *

import os
import sys

# install gdal in virtualenv:
VIRTUAL_ENV = os.environ["VIRTUAL_ENV"]
OSGEO_VENV = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo")
GEOS_LIBRARY_PATH = os.path.join(OSGEO_VENV, "geos_c.dll")
GDAL_LIBRARY_PATH = os.path.join(OSGEO_VENV, "gdal302.dll")
PROJ_LIB = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/proj")

os.environ["GDAL_DATA"] = os.path.join(VIRTUAL_ENV, "Lib/site-packages/osgeo/data/gdal")
os.environ["PROJ_LIB"] = PROJ_LIB
os.environ["PATH"] += os.pathsep + str(OSGEO_VENV)

print("Using main.settngs.test....")
print("sys.path={}".format(sys.path))

SECRET_KEY = "testing_secret_key"

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "fn_portal",
        "USER": get_env_variable("PGUSER"),
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "HOST": "localhost",
    }
}


PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)


COVERAGE_MODULE_EXCLUDES = ["migrations", "fixtures", "admin$", "utils", "config"]
COVERAGE_MODULE_EXCLUDES += THIRD_PARTY_APPS + DJANGO_APPS
# COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(__file__, '../../../coverage')
#
