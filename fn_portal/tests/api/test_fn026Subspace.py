"""=============================================================
~/fn_portal/fn_portal/tests/api/test_fn026Subspace.py
 Created: 21 Sep 2022 16:25:48


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN026Subspace objects works as expected:

  + the fn026subspace list returns all of the subspaces
  associated with a specific project

  + the space detail endpoint will return the project code, space
  code, subspace code, subspace description, dd_lat, dd_lon, slug, and
  id.


=============================================================

"""


import pytest
from django.urls import reverse

from fn_portal.tests.fixtures import api_client, project
from rest_framework import status

from ..factories import FN026Factory


@pytest.mark.django_db
def test_fn026_list(api_client, project):
    """The default FN026Subspace list should return all of the available subspaces."""

    url = reverse("fn_portal_api:subspace_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("subspace"), x.get("subspace_des"), x.get("dd_lat"), x.get("dd_lon"))
        for x in response.data["results"]
    ]
    assert len(data) == 2

    expected = [
        ("ss1", "Subspace 1", 45.11, -81.11),
        ("ss2", "Subspace 2", 45.22, -81.22),
    ]

    assert data == expected


@pytest.mark.django_db
def test_fn026_list_project(api_client, project):
    """The if a project code is supplied to the FN026Subspace list
    endpoint, it should return all of the subspaces within that
    project."""

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:project_subspace_list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("subspace"), x.get("subspace_des"), x.get("dd_lat"), x.get("dd_lon"))
        for x in response.data["results"]
    ]
    assert len(data) == 2

    expected = [
        ("ss1", "Subspace 1", 45.11, -81.11),
        ("ss2", "Subspace 2", 45.22, -81.22),
    ]
    assert data == expected


@pytest.mark.django_db
def test_fn026_list_project_space(api_client, project):
    """The if a project code and a space is supplied to the
    FN026Subspace list endpoint, it should return all of the subspaces
    within that space (for that project).

    """

    prj_cd = project.prj_cd
    space = "S1"
    url = reverse(
        "fn_portal_api:project_space_subspace_list",
        kwargs={"prj_cd": prj_cd, "space": space},
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("subspace"), x.get("subspace_des"), x.get("dd_lat"), x.get("dd_lon"))
        for x in response.data["results"]
    ]
    assert len(data) == 1

    expected = [
        ("ss1", "Subspace 1", 45.11, -81.11),
    ]
    assert data == expected
