"""
The fn_portal filters have a number fo attributes that are associated with the
FN011 table (project attributes). These filters are available on all child
tables.  The tests in this file verify that they work as expected.

A series of project with known attributes are created and then selected by
applying the appropriate filter.   Child fixtures are also created that have one
entry for each project.  We use these child fixtures to verify the projct level
filters select the corresponding child records. e.g. All FN125 records collected in
a specific year.

project level that have filters include:

+ project start and end - gte, lte, exact
+ projct year - gte, gt, lte, lt, exact

+ project code - alone or in a list
+ project code not - alone or in a list
+ project code like
+ project code not like

+ project code ends with string
+ project code does not end with string

+ project name like
+ project name not like

+ project leader

+ protocol - alone and in a list
+ protocol not - alone and in a list

+ lake - alone and in a list
+ lake not - alone and in a list

"""


import pytest
from django.urls import reverse
from rest_framework import status

from .FN011_fixtures import projects, netsets, efforts, catchcounts, fish, age_estimates

filter_args = [
    ({"prj_date0": "2010-10-10"}, [0]),
    ({"prj_date0__lte": "2010-10-10"}, [0, 1, 4, 5]),
    ({"prj_date0__gte": "2010-10-10"}, [0, 2, 3]),
    ({"prj_date1": "2010-10-10"}, [1]),
    ({"prj_date1__lte": "2010-10-10"}, [1, 4, 5]),
    ({"prj_date1__gte": "2010-10-10"}, [0, 1, 2, 3]),
    ({"year": "2010"}, [0, 1]),
    ({"year__gte": "2010"}, [0, 1, 2, 3]),
    ({"year__gt": "2010"}, [2, 3]),
    ({"year__lte": "2010"}, [0, 1, 4, 5]),
    ({"year__lt": "2010"}, [4, 5]),
    ({"prj_cd": "LOA_IA10_000"}, [0]),
    ({"prj_cd": "LOA_IA10_000,LSA_IA07_555"}, [0, 5]),
    ({"prj_cd__not": "LSA_IA08_444"}, [0, 1, 2, 3, 5]),
    ({"prj_cd__not": "LOA_IA10_000,LSA_IA07_555"}, [1, 2, 3, 4]),
    ({"prj_cd__like": "IA10"}, [0, 1]),
    ({"prj_cd__not_like": "IA10"}, [2, 3, 4, 5]),
    ({"prj_cd__endswith": "555"}, [5]),
    ({"prj_cd__not_endswith": "444"}, [0, 1, 2, 3, 5]),
    ({"prj_nm__like": "superior"}, [4, 5]),
    ({"prj_nm__not_like": "superior"}, [0, 1, 2, 3]),
    ({"prj_nm__like": "Superior"}, [4, 5]),
    ({"prj_nm__not_like": "Superior"}, [0, 1, 2, 3]),
    ({"prj_ldr": "hsimpson"}, [0, 1, 5]),
    ({"protocol": "BSM"}, [0, 1, 3]),
    ({"protocol": "BSM,FWIN"}, [0, 1, 2, 3]),
    ({"protocol__not": "BSM"}, [2, 4, 5]),
    ({"protocol__not": "BSM,FWIN"}, [4, 5]),
    ({"lake": "HU"}, [2]),
    ({"lake": "HU,SU"}, [2, 4, 5]),
    ({"lake__not": "HU"}, [0, 1, 3, 4, 5]),
    ({"lake__not": "HU,SU"}, [0, 1, 3]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN011Readonly_filters(client, projects, filter, expected):
    """The readonly api endpoint for FN011 objects accepts a large number
    filters that are associated with attributes of the FN011 table.

    This test is parameterized to accept a list of two element tuples, the
    filter is the filter to apply, the second is the list of indices that
    correspond to the FN011 records that should be returned in the response.
    The indices are used to extract the slugs from the fixture and compare those
    to the slugs returned by the response.

    """

    slugs = []
    for i, x in enumerate(projects):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN121_filters_FN011_attrs(client, netsets, filter, expected):
    """The readonly api endpoint for FN121 objects accepts a large number of
    parameters that are actually attributes of the project (year, project code,
    project lead, start and end date ect.) This test will verify that only net sets
    matching the specified criteria of the project are returned.

    """

    slugs = []
    for i, x in enumerate(netsets):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:netset_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN122_filters_FN011_attrs(client, efforts, filter, expected):
    """The readonly api endpoint for FN122 objects accepts a large number of
    parameters that are actually attributes of the project (year, project code,
    project lead, start and end date ect.) This test will verify that only efforts
    matching the specified criteria of the project are returned.

    """

    slugs = []
    for i, x in enumerate(efforts):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:effort_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN123_filters_FN011_attrs(client, catchcounts, filter, expected):
    """The readonly api endpoint for FN123 objects accepts a large number of
    parameters that are actually attributes of the project (year, project code,
    project lead, start and end date ect.) This test will verify that only efforts
    matching the specified criteria of the project are returned.

    """

    slugs = []
    for i, x in enumerate(catchcounts):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:catchcount_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN125_filters_FN011_attrs(client, fish, filter, expected):
    """The readonly api endpoint for FN125 objects accepts a large number of
    parameters that are actually attributes of the project (year, project code,
    project lead, start and end date ect.) This test will verify that only
    biological samples matching the specified criteria of the project are
    returned.

    """

    slugs = []
    for i, x in enumerate(fish):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:biosample_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN127_filters_FN011_attrs(client, age_estimates, filter, expected):
    """The readonly api endpoint for FN127 objects accepts a large number of
    parameters that are actually attributes of the project (year, project code,
    project lead, start and end date ect.) This test will verify that only age
    estimates matching the specified criteria of the project are returned.

    NOTE - the lamprey, FN125Tags, and FN126 table all share the same filterset
    - if these tests pass, the other child tables will be filtered appropriately
      too.

    """

    slugs = []
    for i, x in enumerate(age_estimates):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn127_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs
