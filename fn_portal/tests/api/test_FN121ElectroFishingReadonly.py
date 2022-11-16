"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121ElectroFishingReadonly.py
 Created: 16 Nov 2022 13:45:37

 DESCRIPTION:

  The FN121ElectroFishing readonly endpoint should return the electrofishinglogical data
  associated with a net set.  the FN121ElectroFishing endpoint accepts a large number
  of filters (url-parameters) assocaited with the electrofishing data, or
  attributes of the net and project. Only fn121electrofishings matching those
  criteria should be returned when query parameters are provided.

=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import FN011Factory, FN121Factory, FN121ElectroFishingFactory


@pytest.fixture
def fn121ElectroFishing_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121a = FN121Factory(project=fn011, sam=1)
    fn121b = FN121Factory(project=fn011, sam=2)

    electrofishing1 = FN121ElectroFishingFactory(sample=fn121a)
    electrofishing2 = FN121ElectroFishingFactory(sample=fn121b)

    return [electrofishing1, electrofishing2]


@pytest.mark.django_db
def test_FN121ElectroFishingReadonly_list(api_client, fn121ElectroFishing_records):
    """when we access the readonly endpoint for FN121ElectroFishing
    objects, it should return a paginated list of fn121electrofishings
    objectsthat includes all of the FN121ElectroFishing objects in the
    database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn121electrofishing_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn121ElectroFishing in fn121ElectroFishing_records:
        assert fn121ElectroFishing.slug in observed


def test_FN121ElectroFishingReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121ElectroFishing readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn121electrofishing_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_FN121ElectroFishingReadonly_expected_keys(
    api_client, fn121ElectroFishing_records
):
    """Verify that the FN121ElectroFishing objects returned by the list view have
    the expected keys.  Especially those that will allow it to be joined
    back up to the parent net set and project.
    """

    url = reverse("fn_portal_api:fn121electrofishing_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    # get the keys from the first object and verify that they match
    # what we expect (at a minimum, we should expect slug, prj_cd and
    # sam will be included in the response:
    observed = payload[0].keys()
    expected = [
        "prj_cd",
        "sam",
        "shock_sec",
        "waveform",
        "volts_min",
        "volts_max",
        "volts_mean",
        "amps_min",
        "amps_max",
        "amps_mean",
        "power_min",
        "power_max",
        "power_mean",
        "conduct",
        "turbidity",
        "pulse_dur",
        "pulse_pattern",
        "freq",
        "anodes",
        "num_netters",
        "comment",
        "slug",
    ]

    assert set(observed) == set(expected)


@pytest.mark.xfail
def test_FN121ElectroFishingReadonly_filters():
    """The readonly api endpoint for FN121ElectroFishing objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121ElectroFishing slugs expected in the
    response.

    """
    assert 0 == 1
