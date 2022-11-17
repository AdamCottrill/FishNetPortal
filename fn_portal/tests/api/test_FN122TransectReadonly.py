"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121GpsTrackReadonly.py
 Created: 03 Jun 2021 11:31:56

 DESCRIPTION:

  The FN121GpsTrack readonly endpoint should return a list of efforts.  The
  list of efforts accepts a large number of filters (url-parameters)
  assocaited with the effort, or attributes of the net and
  project. Only efforts matching those criteria should be returned
  when query parameters are provided.


=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import FN011Factory, FN121Factory, FN121GpsTrackFactory


@pytest.fixture
def fn121_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    track1 = FN121GpsTrackFactory(sample=fn121, track_id=1, sidep=23)
    track2 = FN121GpsTrackFactory(sample=fn121, track_id=2, sidep=25)

    return [track1, track2]


@pytest.mark.django_db
def test_FN121GpsTrackReadonly_list(api_client, fn121_records):
    """when we access the readonly endpoint for FN121GpsTrack objects, it should
    return a paginated list of efforts that includes all of the FN121GpsTrack
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn121_gpstrack_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn121 in fn121_records:
        assert fn121.slug in observed


def test_FN121GpsTrackReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121GpsTrack readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn121_gpstrack_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.xfail
def test_FN121GpsTrackReadonly_filters():
    """The readonly api endpoint for FN121GpsTrack objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121GpsTrack slugs expected in the
    response.

    """
    assert 0 == 1
