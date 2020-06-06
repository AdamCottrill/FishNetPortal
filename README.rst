=====
fn_portal
=====

fn_portal is a Django application that provides an interface and API
for fisheries assessment data collected using the FN-II data model. It
is built as an installable application that can be added to other
projects as needed.  It is currently a mimimum viable product that
provides views and templates for interactive dispay of net sets and
biological attributes of fish by species and project.

More detailed documentation is in the "docs" directory.

Quick start
-----------

0. > pip install tfat.zip

1. Add fn_portal, django restframework, django_filter, and common and
   to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,        
        "rest_framework",
        "rest_framework_swagger",
        "django_filters",
        "common",
        "fn_portal",
    ]

1.1. Install associated dependancies that are not stricly django apps: 
    
2. Include the fn_portal URLconf in your project urls.py like this::

     path("fn_portal/", include(fn_portal_urls, namespace="fn_portal")),
     #optional urls:
     path("api/v1/fn_portal/", include("fn_portal.api.urls", namespace="fn_portal_api")),
     path("docs/", include_docs_urls(title=API_TITLE, description=API_DESC)),
     # path("schema/", schema_view),
     path("swagger-docs/", schema_view),
     
3. Run `python manage.py migrate` to create the fn_portal models.

4. Visit http://127.0.0.1:8000/fn_portal 


Updating the Application
------------------------


Rebuilding the App.
------------------------

FN_PORTAL was built as a standard applicaiton can be rebuild for
distrubition following the instructions found here:

https://docs.djangoproject.com/en/2.2/intro/reusable-apps/

With the fn_portal virtualenv active, and from within the
~/django_fn_portal directory, simply run:

> python setup.py sdist

The package will be placed in the ~/dist folder.  To install the
application run the command:

> pip install fn_portal.zip

To update an existing application issue the command:

> pip install --upgrade fn_portal.zip


Running the tests
------------------------

fn_portal contains a number of unit tests that verify that the
application works as expected and that any regregressions are caught
early. The package uses pytest to run all of the tests, which can be
run by issuing the command:

> pytest

After the tests have completed, coverage reports can be found here:

~/htmlcov

NOTE: you may have to modify the settings GEOS_LIBRARY_PATH and
GDAL_LIBRARY_PATH to point to the locations on your computer for the
tests (and application) to run.
