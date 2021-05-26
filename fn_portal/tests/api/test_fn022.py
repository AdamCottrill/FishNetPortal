"""=============================================================
~/fn_portal/fn_portal/tests/api/test_FN022.py
 Created: 26 May 2021 18:01:09


 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN022 objects works as expected:

  + the fn022 list returns all of the seasons associated with a
  specific project

  + the season detail endpoint will return the ssn, ssn_des, start and
  end date

+ creation rules:
    + must occur before project start and before project endpoint
    + seasons must not overlap - each date can only belong to one season
    + there should not be any gaps - days that do not belong to a season.

 A. Cottrill
=============================================================

"""

import pytest
import json


from django.urls import reverse

from rest_framework import status

from ...models import FN022

from ...tests.fixtures import project, api_client


@pytest.mark.django_db
def test_fn022_list(api_client, project):
    """The FN022 list view should return all of the FN022 objects
    (seasons) asscociated with the project."""

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:fn022-list", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [(x.get("ssn"), x.get("ssn_des")) for x in response.data]
    assert len(data) == 2

    expected = [("32", "August"), ("33", "September")]
    assert data == expected


@pytest.mark.django_db
def test_fn022_detail(api_client, project):
    """The season detail object should return 5 basic elements - the
    project code, season code, season description, start date and end
    date.
    """

    prj_cd = project.prj_cd
    ssn = "32"

    url = reverse("fn_portal_api:fn022-detail", kwargs={"prj_cd": prj_cd, "ssn": ssn})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "project": prj_cd.lower(),
        "ssn": ssn,
        "ssn_des": "August",
        "ssn_date0": "2019-08-01",
        "ssn_date1": "2019-08-31",
    }

    for k, v in expected.items():
        assert response.data[k] == expected[k]


args = [
    ("LHA_IA19_FOO", "33"),  # bad project code, good season
    ("LHA_IA19_000", "99"),  # good project code, bad season
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,ssn", args)
def test_fn022_detail_404(api_client, project, prj_cd, ssn):
    """If we ask for the season of project that does not exist, or season
    that does not exist for a proejct that does, we should get back a 404.

    """

    url = reverse("fn_portal_api:fn022-detail", kwargs={"prj_cd": prj_cd, "ssn": ssn})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
