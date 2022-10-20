"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121TrapnetReadonly.py
 Created: 31 May 2022 13:53:34

 DESCRIPTION:

  The FN121Trapnet readonly endpoint should return the trapnet data
  associated with a net set.  the FN121Trapnet endpoint accepts a large number
  of filters (url-parameters) assocaited with the trapnet data, or
  attributes of the net and project. Only fn121trapnets matching those
  criteria should be returned when query parameters are provided.

=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import FN011Factory, FN121Factory, FN121TrapnetFactory


@pytest.fixture
def fn121Trapnet_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121a = FN121Factory(project=fn011, sam=1)
    fn121b = FN121Factory(project=fn011, sam=2)

    trapnet1 = FN121TrapnetFactory(sample=fn121a)
    trapnet2 = FN121TrapnetFactory(sample=fn121b)

    return [trapnet1, trapnet2]


@pytest.mark.django_db
def test_FN121TrapnetReadonly_list(api_client, fn121Trapnet_records):
    """when we access the readonly endpoint for FN121Trapnet objects, it should
    return a paginated list of fn121trapnets that includes all of the FN121Trapnet
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn121trapnet_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn121Trapnet in fn121Trapnet_records:
        assert fn121Trapnet.slug in observed


def test_FN121TrapnetReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121Trapnet readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn121trapnet_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_FN121TrapnetReadonly_expected_keys(api_client, fn121Trapnet_records):
    """Verify that the FN121Trapnet objects returned by the list view have
    the expected keys.  Especially those that will allow it to be joined
    back up to the parent net set and project.
    """

    url = reverse("fn_portal_api:fn121trapnet_list")
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
        "slug",
        "cover_type",
        "bottom_type",
        "vegetation",
        "lead_angle",
        "leaduse",
        "distoff",
    ]

    assert set(observed) == set(expected)


@pytest.mark.xfail
def test_FN121TrapnetReadonly_filters():
    """The readonly api endpoint for FN121Trapnet objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121Trapnet slugs expected in the
    response.

    """
    assert 0 == 1
