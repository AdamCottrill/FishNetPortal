"""=============================================================
~/fn_portal/fn_portal/tests/api/test_FN013.py
 Created: 08 Jun 2021 17:00:43

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN013 objects works as expected:

  + the fn013 list returns all of the gears associated with a
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

from ...models import FN013

from ...tests.fixtures import project, api_client


@pytest.mark.xfail
@pytest.mark.django_db
def test_fn013_list(api_client, project):
    """The FN013 list view should return all of the FN013 objects
    (gears) asscociated with the project.

    This api endpoint use to return the gear associated with a sigle
    project. The FN013 table not longer exists, as it has been
    superceded by Gear, subgear, etc. THe FN013 list endpoint has been
    created from FN028 objects to maintain consistency with the FN-II
    data model/api.  The FN013 endpoint now returns FN013-like data
    and accepts all of the same filters as the FN208 readonly
    endpoint.

    TODO: modify the FN028-list tests to target then FN013-list
    endpoint and ensure it works as expected and respsects passed in
    filters.

    """

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:fn013_list")
    response = api_client.get(url, {"prj_cd": prj_cd})
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("gr"), x.get("gr_des")) for x in response.data]
    assert len(data) == 2

    expected = [("GL01", "Multifilament"), ("GL32", "Monofilament")]
    assert data == expected


@pytest.mark.django_db
def test_fn013_detail(api_client, project):
    """The gear detail object should return 5 basic elements - the
    project code, gear code, gear description, start date and end
    date.
    """

    prj_cd = project.prj_cd
    gr = "GL01"

    url = reverse("fn_portal_api:fn013-detail", kwargs={"prj_cd": prj_cd, "gr": gr})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "project": prj_cd.lower(),
        "gr": gr,
        "effcnt": 3,
        "effdst": 300,
        "gr_des": "Multifilament",
        "slug": "{}-{}".format(project.slug, gr.lower()),
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]


args = [
    ("LHA_IA19_FOO", "GL10"),  # bad project code, good gear
    ("LHA_IA19_000", "GL99"),  # good project code, bad gear
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,gr", args)
def test_fn013_detail_404(api_client, project, prj_cd, gr):
    """If we ask for the gear of project that does not exist, or gear
    that does not exist for a proejct that does, we should get back a 404.

    """

    url = reverse("fn_portal_api:fn013-detail", kwargs={"prj_cd": prj_cd, "gr": gr})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
