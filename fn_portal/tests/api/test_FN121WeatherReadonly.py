"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121WeatherReadonly.py
 Created: 31 May 2022 13:53:34

 DESCRIPTION:

  The FN121Weather readonly endpoint should return the weather data
  associated with a net set.  the FN121Weather endpoint accepts a large number
  of filters (url-parameters) assocaited with the weather data, or
  attributes of the net and project. Only fn121weathers matching those
  criteria should be returned when query parameters are provided.

=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import (
    FN011Factory,
    FN121Factory,
    FN121WeatherFactory,
)


@pytest.fixture
def fn121Weather_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121a = FN121Factory(project=fn011, sam=1)
    fn121b = FN121Factory(project=fn011, sam=2)

    weather1 = FN121WeatherFactory(
        sample=fn121a,
        wind_speed0="0",
        wind_direction0="0",
        wind_speed1="22",
        wind_direction1="111",
    )
    weather2 = FN121WeatherFactory(sample=fn121b, precip_duration=1, wave_duration=4)

    return [weather1, weather2]


@pytest.mark.django_db
def test_FN121WeatherReadonly_list(api_client, fn121Weather_records):
    """when we access the readonly endpoint for FN121Weather objects, it should
    return a paginated list of fn121weathers that includes all of the FN121Weather
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:fn121weather_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn121Weather in fn121Weather_records:
        assert fn121Weather.slug in observed


def test_FN121WeatherReadonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121Weather readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:fn121weather_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_FN121WeatherReadonly_expected_keys(api_client, fn121Weather_records):
    """Verify that the FN121Weather objects returned by the list view have
    the expected keys.  Especially those that will allow it to be joined
    back up to the parent net set and project.
    """

    url = reverse("fn_portal_api:fn121weather_list")
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
        "airtem0",
        "airtem1",
        "wind0",
        "wind1",
        "precip0",
        "precip1",
        "cloud_pc0",
        "cloud_pc1",
        "waveht0",
        "waveht1",
        "xweather",
    ]

    assert set(observed) == set(expected)


@pytest.mark.django_db
def test_fn121Weather_wind_values(api_client, fn121Weather_records):
    """The api endpoint for weather has some logic in the query set
    that combines wind speed and direction into the expected string
    format.  This test verifies that it returns '000' if both values
    are '0', otherwise it returns them in a formated string: '###-##'
    for direction and speed.

    """

    url = reverse("fn_portal_api:fn121weather_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = payload[0]
    assert observed["wind0"] == "000"
    assert observed["wind1"] == "111-22"


@pytest.mark.django_db
def test_fn121Weather_xweather(api_client, fn121Weather_records):
    """The api endpoint for weather has some logic in the query set
    that combines precip_duration and wave_duration into a single text
    field 'xweather'
    """

    url = reverse("fn_portal_api:fn121weather_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = payload[1]
    # our fixture has precip_duration=1 and wave_duration=4
    assert observed["xweather"] == "14"


@pytest.mark.xfail
def test_FN121WeatherReadonly_filters():
    """The readonly api endpoint for FN121Weather objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121Weather slugs expected in the
    response.

    """
    assert 0 == 1
