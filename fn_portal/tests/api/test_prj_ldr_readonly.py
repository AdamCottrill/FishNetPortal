"""=============================================================
 ~/fn_portal/tests/api/test_prj_ldr_readonly.py
 Created: 20 Sep 2021 15:11:27

 DESCRIPTION:

  The project lead api endpoint should return a list of available
  project leads. by default it only includes active users, but will
  return all users if all=t (or true, or True).  It also has iexact,
  and icontains filters for username, first_name, and last_name

 A. Cottrill
=============================================================

"""

import pytest

from django.urls import reverse

from rest_framework import status

from ..factories import UserFactory
from .fixtures import api_client


@pytest.fixture()
def user_list():
    """ """

    homer = UserFactory(first_name="Homer", last_name="Simpson", username="simpsonho")
    marge = UserFactory(first_name="Marge", last_name="Simpson", username="simpsonma")
    barney = UserFactory(first_name="Barney", last_name="Gumble", username="gumbleba")
    monty = UserFactory(
        first_name="Monty", last_name="Burns", username="burnsmo", is_active=False
    )
    smithers = UserFactory(
        first_name="Waylon",
        last_name="Smithers",
        username="smitherswa",
        is_active=False,
    )

    return [homer, marge, barney, monty, smithers]


@pytest.mark.django_db
def test_prj_ldr_list_active_only(api_client, user_list):
    """If no filters are passed, we expect only active users to be
    returned."""

    url = reverse("fn_portal_api:project_lead_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("username") for x in response.data]

    expected = ["simpsonho", "simpsonma", "gumbleba"]
    assert len(data) == len(expected)
    for x in expected:
        assert x in data


filter_list = [
    # filter, exected users
    ({"all": True}, {"simpsonho", "simpsonma", "gumbleba", "burnsmo", "smitherswa"}),
    (
        {"username": "SimpsonHo"},
        {
            "simpsonho",
        },
    ),
    ({"username__like": "simp"}, {"simpsonho", "simpsonma"}),
    (
        {"first_name": "Homer"},
        {
            "simpsonho",
        },
    ),
    ({"first_name__like": "A"}, {"gumbleba", "simpsonma"}),
    (
        {"last_name": "Gumble"},
        {
            "gumbleba",
        },
    ),
    ({"last_name__like": "Son"}, {"simpsonho", "simpsonma"}),
]


@pytest.mark.parametrize("filter,expected", filter_list)
@pytest.mark.django_db
def test_prj_ldr_list_filters(api_client, user_list, filter, expected):
    """This is a parameterized test that accepts a list of two element
    tuples. The first element of each tuple is a dictionary that specifies
    the filter that should be applied, while the second element contain
    the usernames of the users that should be selected by the filter.
    """

    url = reverse("fn_portal_api:project_lead_list")
    response = api_client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    data = {x.get("username") for x in response.data}
    assert len(data) == len(expected)
    for x in expected:
        assert x in data
