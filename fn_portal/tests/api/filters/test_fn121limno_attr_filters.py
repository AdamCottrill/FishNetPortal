import pytest
from django.urls import reverse
from rest_framework import status

from .FN121Limno_fixtures import limno_data

from .fn121Limno_filter_args import fn121Limno_filter_args as filter_args


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
