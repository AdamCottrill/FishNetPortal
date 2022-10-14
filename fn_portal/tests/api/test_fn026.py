"""=============================================================
~/fn_portal/fn_portal/tests/api/test_FN026.py
 Created: 26 May 2021 18:01:30

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN026 objects works as expected:

  + the fn026 list returns all of the spaces
  associated with a specific project

  + the space detail endpoint will return the space code, space
  description, dd_lat, dd_lon.


=============================================================

"""


import pytest
from django.urls import reverse

from fn_portal.tests.fixtures import api_client, project
from rest_framework import status

from ..factories import FN026Factory


@pytest.mark.django_db
def test_fn026_list(api_client, project):
    """"""

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:fn026-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [
        (x.get("space"), x.get("space_des"), x.get("dd_lat"), x.get("dd_lon"))
        for x in response.data["results"]
    ]
    assert len(data) == 2

    expected = [("S1", "Space 1", 45.1, -81.1), ("S2", "Space 2", 45.2, -81.2)]
    assert data == expected


@pytest.mark.django_db
def test_fn026_detail(api_client, project):
    """"""

    prj_cd = project.prj_cd
    space = "S1"

    expected = {
        "space": "S1",
        "space_des": "Space 1",
        "dd_lat": 45.1,
        "dd_lon": -81.1,
    }

    FN026Factory(project=project, **expected)

    url = reverse(
        "fn_portal_api:fn026-detail", kwargs={"prj_cd": prj_cd, "space": space}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    for k, v in expected.items():
        assert response.data[k] == expected[k]

    expected_fields = {
        "project",
        "label",
        "space",
        "space_des",
        "space_wt",
        "area_lst",
        "grdep_ge",
        "grdep_lt",
        "sidep_lt",
        "sidep_ge",
        "grid_ge",
        "grid_lt",
        "site_lst",
        "sitp_lst",
        "dd_lat",
        "dd_lon",
    }

    assert set(response.data.keys()) == expected_fields


args = [
    ("LHA_IA19_FOO", "S1"),  # bad project code, good space
    ("LHA_IA19_000", "99"),  # good project code, bad space
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,space", args)
def test_fn026_detail_404(api_client, project, prj_cd, space):
    """If we ask for space or project that does exist we should get back a
    404.
    """

    url = reverse(
        "fn_portal_api:fn026-detail", kwargs={"prj_cd": prj_cd, "space": space}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
