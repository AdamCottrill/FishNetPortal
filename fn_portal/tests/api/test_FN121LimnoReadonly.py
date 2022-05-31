"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121LimnoReadonly.py
 Created: 31 May 2022 13:53:34

 DESCRIPTION:

  The FN121Limno readonly endpoint should return the limnological data
  associated with a net set.  the FN121Limno endpoint accepts a large number
  of filters (url-parameters) assocaited with the limno data, or
  attributes of the net and project. Only fn121limnos matching those
  criteria should be returned when query parameters are provided.

=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import FN011Factory, FN121Factory, FN121LimnoFactory


@pytest.fixture
def fn121Limno_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121a = FN121Factory(project=fn011, sam=1)
    fn121b = FN121Factory(project=fn011, sam=2)

    limno1 = FN121LimnoFactory(sample=fn121a)
    limno2 = FN121LimnoFactory(sample=fn121b)

    return [limno1, limno2]


@pytest.mark.django_db
def test_FN121LimnoReadonly_list(api_client, fn121Limno_records):
    """when we access the readonly endpoint for FN121Limno objects, it should
    return a paginated list of fn121limnos that includes all of the FN121Limno
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn121limno_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn121Limno in fn121Limno_records:
        assert fn121Limno.slug in observed


def test_FN121LimnoReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121Limno readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn121limno_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_FN121LimnoReadonly_expected_keys(api_client, fn121Limno_records):
    """Verify that the FN121Limno objects returned by the list view have
    the expected keys.  Especially those that will allow it to be joined
    back up to the parent net set and project.
    """

    url = reverse("fn_portal_api:fn121limno_list")
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
        "do_gear",
        "xo2",
        "xo22",
        "surfdo2",
        "surfdo22",
    ]

    assert set(observed) == set(expected)


@pytest.mark.xfail
def test_FN121LimnoReadonly_filters():
    """The readonly api endpoint for FN121Limno objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121Limno slugs expected in the
    response.

    """
    assert 0 == 1
