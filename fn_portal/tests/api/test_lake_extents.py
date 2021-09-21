"""=============================================================
~/fn_portal/tests/api/test_LakeExtentList.py
 Created: 21 Sep 2021 09:07:16

 DESCRIPTION:

  The Lake extent api endpoint should return a list of our lakes and
  the response should contains lake name, abbrev, and extent of each
  lake. It does not currently accept any filters.

 A. Cottrill
=============================================================

"""

import pytest

from django.contrib.gis.geos import GEOSGeometry
from django.urls import reverse

from rest_framework import status

from ..factories import LakeFactory
from .fixtures import api_client


@pytest.fixture()
def lake_list():
    """A list of lakes with known attributes"""

    hu = LakeFactory(lake_name="Huron", abbrev="HU")
    su = LakeFactory(lake_name="Superior", abbrev="SU")

    return [hu, su]


@pytest.mark.django_db
def test_lake_extent_list(api_client, lake_list):
    """the lake list endpoint should return a response containing one
    element for each lake. Each element should have attributes for the
    lake name, abbrev, and extent.

    """

    url = reverse("fn_portal_api:lake_extent_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.data) == len(lake_list)

    lake = response.data[0]
    assert set(lake.keys()) == {"lake_name", "abbrev", "extent"}
