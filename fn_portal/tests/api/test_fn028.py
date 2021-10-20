"""=============================================================
~/fn_portal/fn_portal/tests/api/test_FN028.py
 Created: 26 May 2021 18:00:57

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN028 objects works as expected:

  + the fn028 list returns all of the fishing modes associated with a
  specific project

  + the mode detail endpoint will return the mode code, mode
  description, dd_lat, dd_lon.

=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from fn_portal.models import FN028


from fn_portal.tests.fixtures import project, api_client


@pytest.mark.django_db
def test_fn028_list(api_client, project):
    """the fn028 list returns all of the fishing modes associated with a
    specific project.
    """

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:fn028-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("mode"), x.get("mode_des")) for x in response.data]
    assert len(data) == 2

    expected = [("m1", "Mode 1"), ("m2", "Mode 2")]
    assert data == expected


@pytest.mark.django_db
def test_fn028_detail(api_client, project):
    """"""
    prj_cd = project.prj_cd
    mode = "m1"

    url = reverse("fn_portal_api:fn028-detail", kwargs={"prj_cd": prj_cd, "mode": mode})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "mode": "m1",
        "mode_des": "Mode 1",
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]


args = [
    ("LHA_IA19_FOO", "m1"),  # bad project code, good mode
    ("LHA_IA19_000", "99"),  # good project code, bad mode
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,mode", args)
def test_fn028_detail_404(api_client, project, prj_cd, mode):
    """If we ask for mode or project that does exist we should get back a
    404.
    """

    url = reverse("fn_portal_api:fn028-detail", kwargs={"prj_cd": prj_cd, "mode": mode})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
