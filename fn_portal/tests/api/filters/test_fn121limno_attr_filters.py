import pytest
from django.urls import reverse
from rest_framework import status

from .FN121Limno_fixtures import limno_data

filter_args = [
    ({"o2gear0": "9.1"}, [1]),
    ({"o2gear0__gte": "9.1"}, [1, 2]),
    ({"o2gear0__lte": "9.1"}, [0, 1, 3]),
    ({"o2gear0__gt": "9.1"}, [2]),
    ({"o2gear0__lt": "9.1"}, [0, 3]),
    ({"o2gear0__null": "true"}, [4, 5]),
    ({"o2gear0__null": "false"}, [0, 1, 2, 3]),
    ({"o2gear0__not_null": "true"}, [0, 1, 2, 3]),
    ({"o2gear0__not_null": "false"}, [4, 5]),
    ({"o2gear1": "9.1"}, [1]),
    ({"o2gear1__gte": "9.1"}, [1, 2]),
    ({"o2gear1__lte": "9.1"}, [0, 1, 3]),
    ({"o2gear1__gt": "9.1"}, [2]),
    ({"o2gear1__lt": "9.1"}, [0, 3]),
    ({"o2gear1__null": "true"}, [4, 5]),
    ({"o2gear1__null": "false"}, [0, 1, 2, 3]),
    ({"o2gear1__not_null": "true"}, [0, 1, 2, 3]),
    ({"o2gear1__not_null": "false"}, [4, 5]),
    ({"o2bot0": 3.3}, [4]),
    ({"o2bot0__gte": 3.3}, [4, 5]),
    ({"o2bot0__lte": 3.3}, [2, 3, 4]),
    ({"o2bot0__gt": 3.3}, [5]),
    ({"o2bot0__lt": 3.3}, [2, 3]),
    ({"o2bot0__null": "true"}, [0, 1]),
    ({"o2bot0__null": "false"}, [2, 3, 4, 5]),
    ({"o2bot0__not_null": "true"}, [2, 3, 4, 5]),
    ({"o2bot0__not_null": "false"}, [0, 1]),
    ({"o2bot1": "7.5"}, [4]),
    ({"o2bot1__gte": "7.5"}, [0, 1, 4]),
    ({"o2bot1__lte": "7.5"}, [4, 5]),
    ({"o2bot1__gt": "7.5"}, [0, 1]),
    ({"o2bot1__lt": "7.5"}, [5]),
    ({"o2bot1__null": "true"}, [2, 3]),
    ({"o2bot1__null": "false"}, [0, 1, 4, 5]),
    ({"o2bot1__not_null": "true"}, [0, 1, 4, 5]),
    ({"o2bot1__not_null": "false"}, [2, 3]),
    ({"o2surf0": "6.7"}, [2]),
    ({"o2surf0__gte": "6.7"}, [2, 3, 5]),
    ({"o2surf0__lte": "6.7"}, [0, 2]),
    ({"o2surf0__gt": "6.7"}, [3, 5]),
    ({"o2surf0__lt": "6.7"}, [0]),
    ({"o2surf0__null": "true"}, [1, 4]),
    ({"o2surf0__null": "false"}, [0, 2, 3, 5]),
    ({"o2surf0__not_null": "true"}, [0, 2, 3, 5]),
    ({"o2surf0__not_null": "false"}, [1, 4]),
    ({"o2surf1": "7.3"}, [3]),
    ({"o2surf1__gte": "7.3"}, [1, 2, 3]),
    ({"o2surf1__lte": "7.3"}, [3, 4]),
    ({"o2surf1__gt": "7.3"}, [1, 2]),
    ({"o2surf1__lt": "7.3"}, [4]),
    ({"o2surf1__null": "true"}, [0, 5]),
    ({"o2surf1__null": "false"}, [1, 2, 3, 4]),
    ({"o2surf1__not_null": "true"}, [1, 2, 3, 4]),
    ({"o2surf1__not_null": "false"}, [0, 5]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN121LimnoReadonly_filters(client, limno_data, filter, expected):
    """The readonly api endpoint for FN121Limno objects accepts a large number
    filters that are associated with attributes of the FN121Limno table.

    This test is parameterized to accept a list of two element tuples, the
    filter is the filter to apply, the second is the list of indices that
    correspond to the FN121Limno records that should be returned in the response.
    The indices are used to extract the slugs from the fixture and compare those
    to the slugs returned by the response.

    """

    slugs = []
    for i, x in enumerate(limno_data):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn121limno_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs
