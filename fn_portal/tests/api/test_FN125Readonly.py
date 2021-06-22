"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN125Readonly.py
 Created: 07 Jun 2021 16:36:52

 DESCRIPTION:

  The FN125 readonly endpoint should return a list of biosamples.  The
  list of biosamples accepts a large number of filters (url-parameters)
  assocaited with the catch, effort, or attributes of the net and
  project. Only biosamples matching those criteria should be returned
  when query parameters are provided.


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
    SpeciesFactory,
)


@pytest.fixture
def fn125_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    eff1 = FN122Factory(sample=fn121, eff="001")

    spc = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )

    catch = FN123Factory(effort=eff1, species=spc, grp="55")

    fish1 = FN125Factory(catch=catch, flen=350, gon=10)
    fish2 = FN125Factory(catch=catch, flen=450, gon=20)
    return [fish1, fish2]


@pytest.mark.django_db
def test_FN125Readonly_list(api_client, fn125_records):
    """when we access the readonly endpoint for FN125 objects, it should
    return a paginated list of lenght tallies that includes all of the FN125
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:biosample_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for record in fn125_records:
        assert record.slug in observed


def test_FN125Readonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN125 readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:biosample_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN
