"""

The tests in this file ensure that the filters associated with the attributes of
the sampled fish (FN125 records) work as expected on the fn125 end point, as
well as the child  tables for lamprey, tags, age estimates, and diet times.  

The fixtures returns an array of fish (or one child element per fish), apply a
filter, and verify that the reponse contains the expected records given the
filter and the attributes of the fish.

"""

import pytest

from rest_framework import status
from django.urls import reverse

from .FN125_fixtures import (
    fish,
    fish_FN125Lamprey,
    fish_FN125Tags,
    fish_FN126,
    fish_FN127,
)

# parameters that will be passed to our FN125 (or lower) api endpoints
# ({filter}, [index of filtered fish])
filter_args = [
    ({"tlen": 350}, [4]),
    ({"tlen__gte": 350}, [2, 3, 4]),
    ({"tlen__lte": 350}, [0, 1, 4, 5]),
    ({"tlen__gt": 350}, [2, 3]),
    ({"tlen__lt": 350}, [0, 1, 5]),
    ({"flen": 325}, [4]),
    ({"flen__gte": 325}, [2, 3, 4]),
    ({"flen__lte": 325}, [0, 1, 4, 5]),
    ({"flen__gt": 325}, [2, 3]),
    ({"flen__lt": 325}, [0, 1, 5]),
    ({"rwt": 800}, [4]),
    ({"rwt__null": True}, [0]),
    ({"rwt__null": False}, [1, 2, 3, 4, 5]),
    ({"rwt__gte": 800}, [2, 3, 4]),
    ({"rwt__lte": 800}, [1, 4, 5]),
    ({"rwt__gt": 800}, [2, 3]),
    ({"rwt__lt": 800}, [1, 5]),
    ({"sex": 1}, [1, 2]),
    ({"sex": "1,9"}, [0, 1, 2]),
    ({"sex__null": True}, [4, 5]),
    ({"sex__null": False}, [0, 1, 2, 3]),
    (
        {"gon": 10},
        [
            2,
        ],
    ),
    ({"gon": "20,30"}, [3, 4]),
    ({"gon__null": True}, [0, 1]),
    ({"gon__null": False}, [2, 3, 4, 5]),
    ({"mat": 1}, [2]),
    ({"mat": "1,2"}, [2, 3]),
    ({"mat__null": True}, [1, 4]),
    ({"mat__null": False}, [0, 2, 3, 5]),
    ({"clipc": 0}, [0, 3]),
    ({"clipc": "1,5"}, [1, 2]),
    ({"clipc__null": True}, [5]),
    ({"clipc__null": False}, [0, 1, 2, 3, 4]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN125Readonly_filters(client, fish, filter, expected):
    """The readonly api endpoint for FN125 objects accepts a large number
    of potential parameters as filters. This test will verify that only
    catch counts matching the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN125 slugs expected in the
    response.

    """

    slugs = []
    for i, x in enumerate(fish):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:biosample_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the repsonse:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN125Lamprey_filters_fish_attrs(client, fish_FN125Lamprey, filter, expected):
    """The readonly api endpoint for FN125Lamprey objects accepts a large number
    of potential parameters that are actually attributes of the parent fish
    (size, sex, maturity, clipc etc). This test will verify that only wounds
    matching the specified criteria of the parent fish are returned.

    This test is parameterized with a list of two element tuples, the filter to
    apply, and a list of the arrary indices that correspond to the array of
    lamprey wounds.    We compare the slugs from our array with the slugs returned in the response.

    """

    slugs = []
    for i, x in enumerate(fish_FN125Lamprey):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn125lamprey_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the repsonse:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN125tag_filters_fish_attrs(client, fish_FN125Tags, filter, expected):
    """The readonly api endpoint for FN125tag objects accepts a large number of
    parameters that are actually attributes of the parent fish (size, sex,
    maturity, clipc etc). This test will verify that only tags matching the
    specified criteria of the parent fish are returned.

    This test is parameterized with a list of two element tuples, the filter to
    apply, and a list of the arrary indices that correspond to the array of tags
    created in the fixture (one for each fish). We compare the slugs from our
    array with the slugs returned in the response.

    """

    slugs = []
    for i, x in enumerate(fish_FN125Tags):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn125tags_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the repsonse:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN126_filters_fish_attrs(client, fish_FN126, filter, expected):
    """The readonly api endpoint for FN126 objects accepts a large number of
    parameters that are actually attributes of the parent fish (size, sex,
    maturity, clipc etc). This test will verify that only diet items matching the
    specified criteria of the parent fish are returned.

    This test is parameterized with a list of two element tuples, the filter to
    apply, and a list of the arrary indices that correspond to the array of diet items
    created in the fixture (one for each fish). We compare the slugs from our
    array with the slugs returned in the response.

    """

    slugs = []
    for i, x in enumerate(fish_FN126):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn126_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the repsonse:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN127_filters_fish_attrs(client, fish_FN127, filter, expected):
    """The readonly api endpoint for FN127 objects accepts a large number of
    parameters that are actually attributes of the parent fish (size, sex,
    maturity, clipc etc). This test will verify that only age estimates matching the
    specified criteria of the parent fish are returned.

    This test is parameterized with a list of two element tuples, the filter to
    apply, and a list of the arrary indices that correspond to the array of age estimates
    created in the fixture (one for each fish). We compare the slugs from our
    array with the slugs returned in the response.

    """

    slugs = []
    for i, x in enumerate(fish_FN127):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn127_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the repsonse:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs