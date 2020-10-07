"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/fn_portal/tests/api/test_species_list.py
 Created: 22 Sep 2020 15:57:50

 DESCRIPTION:

  This script verifies that the species_list api endpoint returns the
  exected values and acccomdates filters for species, common name, and
  scientific_name.

 A. Cottrill
=============================================================

"""


import pytest
from django.urls import reverse

from rest_framework import status

from ..factories import SpeciesFactory
from .fixtures import api_client


@pytest.fixture
def species_list():
    """
    """

    spc_081 = (
        SpeciesFactory(
            spc="081", spc_nmco="lake trout", spc_nmsc="Salvelinus namaycush"
        ),
    )
    spc_091 = (
        SpeciesFactory(
            spc="091", spc_nmco="lake whitefish", spc_nmsc="Coregonus clupeaformis"
        ),
    )
    spc_093 = SpeciesFactory(
        spc="093", spc_nmco="cisco", spc_nmsc="Coregonus clupeaformis"
    )

    return [spc_081, spc_091, spc_093]


@pytest.mark.django_db
def test_species_listview(api_client, species_list):
    """The species listview should return a json resposne containing all of
    the species in our database

    It should be available to any user.
    """

    url = reverse("fn_portal_api:species_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("spc") for x in response.data["results"]]

    assert len(data) == 3

    expected = ["081", "091", "093"]
    for x in expected:
        assert x in data


@pytest.mark.django_db
def test_species_listview_spc_filter(api_client, species_list):
    """If our url contains a query parameter for spc, only those species
    that have spc code in the query string should be returned in the
    json response. ()

    """

    q = "?spc=081,091"
    url = reverse("fn_portal_api:species_list")
    response = api_client.get(url + q)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("spc") for x in response.data["results"]]

    assert len(data) == 2

    expected = ["081", "091"]
    for x in expected:
        assert x in data


spc_nmco_list = ["lake", "LAKE", "LaKe"]


@pytest.mark.parametrize("value", spc_nmco_list)
@pytest.mark.django_db
def test_species_listview_nmco_filter(api_client, species_list, value):
    """If our url contains a query parameter for common name, only those
    species that part of the specified string in their common name
    should be returned. The match should not be case sensitive.

    """

    q = "?spc_nmco_like={}".format(value)
    url = reverse("fn_portal_api:species_list")
    response = api_client.get(url + q)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("spc") for x in response.data["results"]]

    assert len(data) == 2

    # we should see *lake* trout and *lake* whitefish
    expected = ["081", "091"]
    for x in expected:
        assert x in data


spc_nmsc_list = ["Coregonus", "COREGONUS", "CorEgONus"]


@pytest.mark.parametrize("value", spc_nmsc_list)
@pytest.mark.django_db
def test_species_listview_nmsc_filter(api_client, species_list, value):
    """If our url contains a query parameter for scientific_name name, only those
    species that part of the specified string in their scientific name
    should be returned. The match should not be case sensitive.

    """

    q = "?spc_nmsc_like={}".format(value)
    url = reverse("fn_portal_api:species_list")
    response = api_client.get(url + q)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("spc") for x in response.data["results"]]

    assert len(data) == 2

    # we should see whitefish(*Coregonus* clupeaformis) and herring (*Coregonus* artedi)
    expected = ["091", "093"]
    for x in expected:
        assert x in data
