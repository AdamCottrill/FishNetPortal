"""=============================================================
 ~/fn_portal/tests/api/test_FNProtocolList.py
 Created: 21 Sep 2021 11:04:59

 DESCRIPTION:

  The protocol list api endpoint should return a list of available
  protocols. By default it should only include active, documented
  protocols but will return all protocols if all=t (or true, or
  True). It will return active/inactive protocols if 'active' is
  provided (as a boolean), and will return protocols that are
  confirmed (or unconfirmed) if 'confirmed' is provided as a boolean.

 A. Cottrill
=============================================================

"""

import pytest

from django.urls import reverse

from rest_framework import status

from ..factories import FNProtocolFactory
from .fixtures import api_client


@pytest.fixture()
def protocol_list():
    """A list of protocol with known attributes"""

    bsm = FNProtocolFactory(abbrev="BSM", confirmed=True, active=True)
    slin = FNProtocolFactory(abbrev="SLIN", confirmed=True, active=True)
    fwin = FNProtocolFactory(abbrev="FWIN", confirmed=True, active=False)
    wtf = FNProtocolFactory(abbrev="WTF", confirmed=False, active=True)
    unkn = FNProtocolFactory(abbrev="UNKN", confirmed=False, active=False)

    return [bsm, slin, fwin, wtf, unkn]


@pytest.mark.django_db
def test_protocol_list_default(api_client, protocol_list):
    """If no filters are passed in, we expect protocol list endpoint to only
    include active protocols (deprecieated=False) that have been confirmed.

    """

    url = reverse("fn_portal_api:protocol_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("abbrev") for x in response.data]

    expected = ["BSM", "SLIN"]
    assert len(data) == len(expected)
    for x in expected:
        assert x in data


filter_list = [
    # filter, exected protocols
    ({"all": True}, {"BSM", "SLIN", "FWIN", "WTF", "UNKN"}),
    ({"confirmed": True}, {"BSM", "SLIN"}),
    ({"confirmed": False}, {"WTF"}),
    ({"active": True}, {"BSM", "SLIN"}),
    ({"active": False}, {"FWIN"}),
    ({"active": False, "confirmed": False}, {"UNKN"}),
]


@pytest.mark.parametrize("filter,expected", filter_list)
@pytest.mark.django_db
def test_protocol_list_filters(api_client, protocol_list, filter, expected):
    """This is a parameterized test that accepts a list of two element
    tuples. The first element of each tuple is a dictionary that specifies
    the filter that should be applied, while the second element contains
    the protocol abbrev of the protocol that should be selected by the filter.
    """

    url = reverse("fn_portal_api:protocol_list")
    response = api_client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    data = {x.get("abbrev") for x in response.data}
    assert len(data) == len(expected)
    for x in expected:
        assert x in data
