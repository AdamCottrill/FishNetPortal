"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN125LampreyReadonly.py
 Created: 07 Jun 2021 16:36:52

 DESCRIPTION:

  The FN125Lamprey readonly endpoint should return a list of lamprey
  wounds that have either been observed on sampled fish.  The
  fn125Lamprey_list end point accepts a large number of filters
  (url-parameters) assocaited with the lamprey wound, the sampled fish, the
  catch, effort, or attributes of the net and project. Only diet items
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
    FN125LampreyFactory,
    SpeciesFactory,
)


@pytest.fixture
def fn125lamprey_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    eff1 = FN122Factory(sample=fn121, eff="001")

    spc = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )

    catch = FN123Factory(effort=eff1, species=spc, grp="55")

    fish = FN125Factory(catch=catch, flen=350, gon=10)
    lamprey1 = FN125LampreyFactory(fish=fish, lamijc_type="A1", lamijc_size=30)
    lamprey2 = FN125LampreyFactory(fish=fish, lamijc_type="B2", lamijc_size=25)
    return [lamprey1, lamprey2]


@pytest.mark.django_db
def test_FN125lampreyReadonly_list(api_client, fn125lamprey_records):
    """when we access the readonly endpoint for FN125lamprey objects, it should
    return a paginated list of lamprey wounds that includes all of the FN125lamprey
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn125lamprey_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for record in fn125lamprey_records:
        assert record.slug in observed


def test_FN125lampreyReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN125lamprey readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn125lamprey_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.xfail
def test_FN125lampreyReadonly_filters():
    """The readonly api endpoint for FN125lamprey objects accepts a large number
    of potential parameters as filters. This test will verify that only
    lamprey matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN125lamprey slugs expected in the
    response.

    """
    assert 0 == 1
