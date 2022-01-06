"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN126Readonly.py
 Created: 07 Jun 2021 16:36:52

 DESCRIPTION:

  The FN126 readonly endpoint should return a list of diet items found
  in sampled fish.  The fn126_list end point accepts a large number of
  filters (url-parameters) assocaited with the sample fish, the catch,
  effort, or attributes of the net and project. Only diet items
  matching those criteria should be returned when query parameters are
  provided.


=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import (
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
    FN126Factory,
    SpeciesFactory,
)


@pytest.fixture
def fn126_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    eff1 = FN122Factory(sample=fn121, eff="001")

    spc = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )

    catch = FN123Factory(effort=eff1, species=spc, grp="55")

    fish = FN125Factory(catch=catch, flen=350, gon=10)
    food1 = FN126Factory(fish=fish, taxon="F061", fdcnt=10)
    food2 = FN126Factory(fish=fish, taxon="F121", fdcnt=20)
    return [food1, food2]


@pytest.mark.django_db
def test_FN126Readonly_list(api_client, fn126_records):
    """when we access the readonly endpoint for FN126 objects, it should
    return a paginated list of diet item that includes all of the FN126
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn126_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for record in fn126_records:
        assert record.slug in observed


def test_FN126Readonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN126 readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn126_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.xfail
def test_FN126Readonly_filters():
    """The readonly api endpoint for FN126 objects accepts a large number
    of potential parameters as filters. This test will verify that only
    catch counts matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN126 slugs expected in the
    response.

    """
    assert 0 == 1
