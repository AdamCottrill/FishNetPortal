"""=============================================================
~/fn_portal/fn_portal/tests/api/test_FN014.py
 Created: 08 Jun 2021 17:00:43

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN014 objects works as expected:

  + the fn014 list returns all of the gears associated with a
  specific project

  + the gear detail endpoint will return the attributes of ssn, ssn_des, start and
  end date

+ creation rules:
    + must occur before project start and before project endpoint
    + gears must not overlap - each date can only belong to one gear
    + there should not be any gaps - days that do not belong to a gear.


=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from ...models import FN014

from ...tests.fixtures import project, api_client


@pytest.mark.django_db
def test_fn014_list(api_client, project):
    """The FN014 list view should return all of the FN014 objects
    (sub-gear elements) asscociated with a gear used in a  project."""

    prj_cd = project.prj_cd
    gr = "GL01"

    url = reverse("fn_portal_api:fn014-list", kwargs={"prj_cd": prj_cd, "gr": gr})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("eff"), x.get("mesh"), x.get("grlen")) for x in response.data]
    assert len(data) == 3
    expected = [
        ("038", 38, 100),
        ("051", 51, 100),
        ("064", 64, 100),
    ]
    assert data == expected


@pytest.mark.django_db
def test_fn014_detail(api_client, project):
    """The gear detail object should return 5 basic elements - the
    project code, gear code, gear description, start date and end
    date.
    """

    prj_cd = project.prj_cd
    gr = "GL01"
    eff = "038"
    url = reverse(
        "fn_portal_api:fn014-detail", kwargs={"prj_cd": prj_cd, "gr": gr, "eff": eff}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    print(response.data)

    expected_keys = {
        "gear",
        "eff",
        "mesh",
        "grlen",
        "grht",
        "grwid",
        "grcol",
        "grmat",
        "gryarn",
        "grknot",
        "eff_des",
        "slug",
    }

    assert set(response.data.keys()) == expected_keys

    expected = {
        "eff": "038",
        "mesh": 38,
        "grlen": 100,
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]


args = [
    ("LHA_IA19_FOO", "GL01", "038"),  # bad project code, good gear, good effort
    ("LHA_IA19_000", "GL99", "038"),  # good project code, bad gear, good effort
    ("LHA_IA19_000", "GL01", "999"),  # good project code, good gear, bad effort
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,gr,eff", args)
def test_fn014_detail_404(api_client, project, prj_cd, gr, eff):
    """If we ask for the gear of project that does not exist, or gear
    that does not exist for a proejct that does, we should get back a 404.

    """

    url = reverse(
        "fn_portal_api:fn014-detail", kwargs={"prj_cd": prj_cd, "gr": gr, "eff": eff}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
