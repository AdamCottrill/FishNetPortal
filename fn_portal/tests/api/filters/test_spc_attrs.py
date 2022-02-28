"""
    The readonly api endpoint for FN012 objects accepts a several
    parameters that are actually attributes of the species - species
    code, species name, or scientific name This test will verify that
    only sampling constraints matching the specified criteria of the
    project are returned.

"""


import pytest
from django.urls import reverse
from rest_framework import status

from .FN011_fixtures import (
    projects,
    sample_specs,
)


filter_args = [
    ({"spc": "091"}, [3]),
    ({"spc__not": "091"}, [0, 1, 2, 4, 5]),
    ({"spc": "331,334"}, [4, 5]),
    ({"spc__not": "331,334"}, [0, 1, 2, 3]),
    ({"spc_nmco__like": "trout"}, [1, 2]),
    ({"spc_nmco__not_like": "trout"}, [0, 3, 4, 5]),
    ({"spc_nmsc__like": "Oncorhynchus"}, [0, 1]),
    ({"spc_nmsc__not_like": "Oncorhynchus"}, [2, 3, 4, 5]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN012_filters_spc_attrs(client, sample_specs, filter, expected):

    """The readonly api endpoint for FN012 objects accepts a several
    parameters that are actually attributes of the species - species
    code, species name, or scientific name This test will verify that
    only sampling constraints matching the specified criteria of the
    project are returned.

    """

    slugs = []
    for i, x in enumerate(sample_specs):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:sample_specs_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs
