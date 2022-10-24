import pytest
from django.urls import reverse
from rest_framework import status

from ...factories import FN011Factory, FN121Factory, FN121WeatherFactory


# precip0 an precip1
# wind_direction0 and wind_direction1
# cloud_pc0 an cloud_pc1
# wave_duration
# waveht_duration


@pytest.fixture
def weather_data():
    """create several sets of with known attributes and return them in an
    array"""

    project = FN011Factory()
    sample1 = FN121Factory(project=project)
    weather1 = FN121WeatherFactory(
        sample=sample1,
        airtem0=8.1,
        airtem1=8.1,
        wind_speed0=None,
        wind_direction0=None,
        wind_speed1=25,
        wind_direction1=90,
        waveht0=2.7,
        waveht1=None,
        cloud_pc0=10,
        cloud_pc1=50,
    )

    sample2 = FN121Factory(project=project)
    weather2 = FN121WeatherFactory(
        sample=sample2,
        airtem0=9.1,
        airtem1=9.1,
        wind_speed0=None,
        wind_direction0=None,
        wind_speed1=15,
        wind_direction1=270,
        waveht0=None,
        waveht1=1.3,
        cloud_pc0=0,
        cloud_pc1=50,
    )

    sample3 = FN121Factory(project=project)
    weather3 = FN121WeatherFactory(
        sample=sample3,
        airtem0=14.0,
        airtem1=14.0,
        wind_speed0=11,
        wind_direction0=90,
        wind_speed1=None,
        wind_direction1=None,
        waveht0=1.7,
        waveht1=0.5,
        cloud_pc0=90,
        cloud_pc1=75,
    )

    sample4 = FN121Factory(project=project)
    weather4 = FN121WeatherFactory(
        sample=sample4,
        airtem0=4.0,
        airtem1=4.0,
        wind_speed0=12,
        wind_direction0=45,
        wind_speed1=None,
        wind_direction1=None,
        waveht0=0.7,
        waveht1=0.3,
        cloud_pc0=None,
        cloud_pc1=25,
    )

    sample5 = FN121Factory(project=project)
    weather5 = FN121WeatherFactory(
        sample=sample5,
        airtem0=None,
        airtem1=None,
        wind_speed0=25,
        wind_direction0=90,
        wind_speed1=15,
        wind_direction1=90,
        waveht0=None,
        waveht1=0.3,
        cloud_pc0=25,
        cloud_pc1=None,
    )

    sample6 = FN121Factory(project=project)
    weather6 = FN121WeatherFactory(
        sample=sample6,
        airtem0=None,
        airtem1=None,
        wind_speed0=4,
        wind_direction0=360,
        wind_speed1=6,
        wind_direction1=15,
        waveht0=0.7,
        waveht1=None,
        cloud_pc0=100,
        cloud_pc1=0,
    )

    return [weather1, weather2, weather3, weather4, weather5, weather6]


filter_args = [
    ({"airtem0": "9.1"}, [1]),
    ({"airtem0__gte": "9.1"}, [1, 2]),
    ({"airtem0__lte": "9.1"}, [0, 1, 3]),
    ({"airtem0__gt": "9.1"}, [2]),
    ({"airtem0__lt": "9.1"}, [0, 3]),
    ({"airtem0__null": "true"}, [4, 5]),
    ({"airtem0__null": "false"}, [0, 1, 2, 3]),
    ({"airtem0__not_null": "true"}, [0, 1, 2, 3]),
    ({"airtem0__not_null": "false"}, [4, 5]),
    ({"airtem1": "9.1"}, [1]),
    ({"airtem1__gte": "9.1"}, [1, 2]),
    ({"airtem1__lte": "9.1"}, [0, 1, 3]),
    ({"airtem1__gt": "9.1"}, [2]),
    ({"airtem1__lt": "9.1"}, [0, 3]),
    ({"airtem1__null": "true"}, [4, 5]),
    ({"airtem1__null": "false"}, [0, 1, 2, 3]),
    ({"airtem1__not_null": "true"}, [0, 1, 2, 3]),
    ({"airtem1__not_null": "false"}, [4, 5]),
    ({"wind_speed0": 11}, [2]),
    ({"wind_speed0__gte": 11}, [2, 3, 4]),
    ({"wind_speed0__lte": 11}, [2, 5]),
    ({"wind_speed0__gt": 11}, [3, 4]),
    ({"wind_speed0__lt": 11}, [5]),
    ({"wind_speed0__null": "true"}, [0, 1]),
    ({"wind_speed0__null": "false"}, [2, 3, 4, 5]),
    ({"wind_speed0__not_null": "true"}, [2, 3, 4, 5]),
    ({"wind_speed0__not_null": "false"}, [0, 1]),
    ({"wind_speed1": "15"}, [1, 4]),
    ({"wind_speed1__gte": "15"}, [0, 1, 4]),
    ({"wind_speed1__lte": "15"}, [1, 4, 5]),
    (
        {"wind_speed1__gt": "15"},
        [
            0,
        ],
    ),
    (
        {"wind_speed1__lt": "15"},
        [
            5,
        ],
    ),
    ({"wind_speed1__null": "true"}, [2, 3]),
    ({"wind_speed1__null": "false"}, [0, 1, 4, 5]),
    ({"wind_speed1__not_null": "true"}, [0, 1, 4, 5]),
    ({"wind_speed1__not_null": "false"}, [2, 3]),
    ({"wind_direction0": 90}, [2, 4]),
    ({"wind_direction0__gte": 90}, [2, 4, 5]),
    ({"wind_direction0__lte": 90}, [2, 3, 4]),
    ({"wind_direction0__gt": 90}, [5]),
    ({"wind_direction0__lt": 90}, [3]),
    ({"wind_direction0__null": "true"}, [0, 1]),
    ({"wind_direction0__null": "false"}, [2, 3, 4, 5]),
    ({"wind_direction0__not_null": "true"}, [2, 3, 4, 5]),
    ({"wind_direction0__not_null": "false"}, [0, 1]),
    ({"wind_direction1": 90}, [0, 4]),
    ({"wind_direction1__gte": 90}, [0, 1, 4]),
    ({"wind_direction1__lte": 90}, [0, 4, 5]),
    ({"wind_direction1__gt": 90}, [1]),
    ({"wind_direction1__lt": 90}, [5]),
    ({"wind_direction1__null": "true"}, [2, 3]),
    ({"wind_direction1__null": "false"}, [0, 1, 4, 5]),
    ({"wind_direction1__not_null": "true"}, [0, 1, 4, 5]),
    ({"wind_direction1__not_null": "false"}, [2, 3]),
    ({"waveht0": "1.7"}, [2]),
    ({"waveht0__gte": "1.7"}, [0, 2]),
    ({"waveht0__lte": "1.7"}, [2, 3, 5]),
    (
        {"waveht0__gt": "1.7"},
        [
            0,
        ],
    ),
    ({"waveht0__lt": "1.7"}, [3, 5]),
    ({"waveht0__null": "true"}, [1, 4]),
    ({"waveht0__null": "false"}, [0, 2, 3, 5]),
    ({"waveht0__not_null": "true"}, [0, 2, 3, 5]),
    ({"waveht0__not_null": "false"}, [1, 4]),
    ({"waveht1": "0.5"}, [2]),
    ({"waveht1__gte": "0.5"}, [1, 2]),
    ({"waveht1__lte": "0.5"}, [2, 3, 4]),
    (
        {"waveht1__gt": "0.5"},
        [
            1,
        ],
    ),
    ({"waveht1__lt": "0.5"}, [3, 4]),
    ({"waveht1__null": "true"}, [0, 5]),
    ({"waveht1__null": "false"}, [1, 2, 3, 4]),
    ({"waveht1__not_null": "true"}, [1, 2, 3, 4]),
    ({"waveht1__not_null": "false"}, [0, 5]),
    ({"cloud_pc0": 25}, [4]),
    ({"cloud_pc0__gte": 25}, [2, 4, 5]),
    ({"cloud_pc0__lte": 25}, [0, 1, 4]),
    ({"cloud_pc0__gt": 25}, [2, 5]),
    ({"cloud_pc0__lt": 25}, [0, 1]),
    (
        {"cloud_pc0__null": "true"},
        [
            3,
        ],
    ),
    ({"cloud_pc0__null": "false"}, [0, 1, 2, 4, 5]),
    ({"cloud_pc0__not_null": "true"}, [0, 1, 2, 4, 5]),
    (
        {"cloud_pc0__not_null": "false"},
        [
            3,
        ],
    ),
    ({"cloud_pc1": 50}, [0, 1]),
    (
        {"cloud_pc1__gte": 50},
        [
            0,
            1,
            2,
        ],
    ),
    ({"cloud_pc1__lte": 50}, [0, 1, 3, 5]),
    ({"cloud_pc1__gt": 50}, [2]),
    ({"cloud_pc1__lt": 50}, [3, 5]),
    (
        {"cloud_pc1__null": "true"},
        [
            4,
        ],
    ),
    ({"cloud_pc1__null": "false"}, [0, 1, 2, 3, 5]),
    ({"cloud_pc1__not_null": "true"}, [0, 1, 2, 3, 5]),
    (
        {"cloud_pc1__not_null": "false"},
        [
            4,
        ],
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN121WeatherReadonly_filters(client, weather_data, filter, expected):
    """The readonly api endpoint for FN121Weather objects accepts a large number
    filters that are associated with attributes of the FN121Weather table.

    This test is parameterized to accept a list of two element tuples, the
    filter is the filter to apply, the second is the list of indices that
    correspond to the FN121Weather records that should be returned in the response.
    The indices are used to extract the slugs from the fixture and compare those
    to the slugs returned by the response.

    """

    slugs = []
    for i, x in enumerate(weather_data):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn121weather_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs
