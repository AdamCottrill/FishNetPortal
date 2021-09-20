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

0. > pip install fn_portal.zip

1. Add fn_portal, django restframework, django_filter, drf_yasg and common and
   to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "rest_framework",
        "rest_framework_swagger",
        "django_filters",
        "common",
        "fn_portal",
        "drf_yasg"
    ]

1.1. Install associated dependancies that are not stricly django apps:

2. Include the fn_portal URLconf in your project urls.py like this::

     path("fn_portal/", include(fn_portal_urls, namespace="fn_portal")),

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


Update the Documentation
------------------------

The documentation for FN_portal has been created using sphinx. The
source code for the documentation can be found in the ~/docs directory.

sphinx-autobuild is included in the local requirements file.  To
automatically rebuild the documentation during development follow
these steps in a command window:

1. navigate to the root fn_portal directory
2. activate the fn_portal virtual environment
3. run:

.. code:: bash

   > sphinx-autobuild docs/sphinx/source  docs/sphinx/build/html

The documentation should be available in you browser at 127.0.0.1:8000
(which can be changed by passing addition command line arguments).
The documentation will be updated dynamically as the source files are
changed.




Running the tests
-----------------

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
