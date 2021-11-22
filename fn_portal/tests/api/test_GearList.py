"""=============================================================
~/fn_portal/tests/api/test_GearList.py
 Created: 21 Sep 2021 09:07:16

 DESCRIPTION:

  The gear list api endpoint should return a list of available
  gears. By default it should only include active, documented gears
  but will return all gears if all=t (or true, or True).  It also has
  filters for gear type, gear code 'like' and gear code in.

 A. Cottrill
=============================================================

"""

import pytest

from django.urls import reverse

from rest_framework import status

from ..factories import GearFactory, GearEffortProcessTypeFactory
from .fixtures import api_client


@pytest.fixture()
def gear_list():
    """A list of gear with known attributes"""

    gl00 = GearFactory(gr_code="GL00", grtp="GL", confirmed=False, depreciated=True)
    gl01 = GearFactory(gr_code="GL01", grtp="GL", confirmed=True, depreciated=True)
    gl21 = GearFactory(gr_code="GL21", grtp="GL", confirmed=True, depreciated=False)
    gl32 = GearFactory(gr_code="GL32", grtp="GL", confirmed=True, depreciated=False)
    gl50 = GearFactory(gr_code="GL50", grtp="GL", confirmed=True, depreciated=False)
    tp01 = GearFactory(gr_code="TP01", grtp="TP", confirmed=False, depreciated=True)
    tp08 = GearFactory(gr_code="TP08", grtp="TP", confirmed=True, depreciated=False)

    GearEffortProcessTypeFactory(gear=gl00)
    GearEffortProcessTypeFactory(gear=gl01)
    GearEffortProcessTypeFactory(gear=gl21)
    GearEffortProcessTypeFactory(gear=gl32)
    GearEffortProcessTypeFactory(gear=gl50)
    GearEffortProcessTypeFactory(gear=tp01)
    GearEffortProcessTypeFactory(gear=tp08)

    return [gl00, gl01, gl21, gl32, gl50, tp01, tp08]


@pytest.mark.django_db
def test_gear_list_default(api_client, gear_list):
    """If no filters are passed in, we expect gear list endpoint to only
    include active gears (deprecieated=False) that have been confirmed.

    """

    url = reverse("fn_portal_api:gear_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("gr_code") for x in response.data]

    expected = ["GL21", "GL32", "GL50", "TP08"]
    assert len(data) == len(expected)
    for x in expected:
        assert x in data


filter_list = [
    # filter, exected users
    ({"all": True}, {"GL00", "GL01", "GL21", "GL32", "GL50", "TP01", "TP08"}),
    ({"confirmed": True}, {"GL21", "GL32", "GL50", "TP08"}),
    # there are no active gears that have not been confirmed
    ({"confirmed": False}, {}),
    # confirmed implied:
    ({"depreciated": True}, {"GL01"}),
    ({"depreciated": False}, {"GL21", "GL32", "GL50", "TP08"}),
    ({"depreciated": True, "confirmed": False}, {"GL00", "TP01"}),
    ({"grtp": "Tp"}, {"TP08"}),
    ({"gr__like": "2"}, {"GL21", "GL32"}),
    ({"gr": "GL21,TP08"}, {"GL21", "TP08"}),
    ({"gr": "GL32"}, {"GL32"}),
]


@pytest.mark.parametrize("filter,expected", filter_list)
@pytest.mark.django_db
def test_gear_list_filters(api_client, gear_list, filter, expected):
    """This is a parameterized test that accepts a list of two element
    tuples. The first element of each tuple is a dictionary that specifies
    the filter that should be applied, while the second element contain
    the gear code of the gear that should be selected by the filter.
    """

    url = reverse("fn_portal_api:gear_list")
    response = api_client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    data = {x.get("gr_code") for x in response.data}
    assert len(data) == len(expected)
    for x in expected:
        assert x in data


@pytest.mark.django_db
def test_gear_process_type_in_response(api_client):
    """The known process types for each gear are returned as children of
    the gear in the response. This test ensure that there is a key called 'process type'
    and that it has the expected data.

    """

    process_types = [
        {"eff": "001", "process_type": "1"},
        {"eff": "001", "process_type": "3"},
        {"eff": "002", "process_type": "3"},
    ]

    gear = GearFactory()
    for ptype in process_types:
        GearEffortProcessTypeFactory(gear=gear, **ptype)

    url = reverse("fn_portal_api:gear_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    observed = response.data[0]["process_types"]

    # the response includes the label for each process type - we need
    # to add them to our expected values:
    labels = ["By Sample", "By Panel Group", "By Panel Group"]
    for item, label in zip(process_types, labels):
        item["label"] = label

    assert observed == process_types


@pytest.mark.parametrize("filter,expected", filter_list)
@pytest.mark.django_db
def test_gear_process_type_in_response_filters(api_client, gear_list, filter, expected):
    """This is a parameterized test that accepts a list of two element
    tuples. The first element of each tuple is a dictionary that
    specifies the filter that should be applied, while the second
    element contain the gear code of the gear that should be selected
    by the filter.  This test uses the same filters as the gear code
    list, but applies them to the gear-effort-process-type endpoint to
    ensure that the same filters apply there.



    """

    url = reverse("fn_portal_api:gear_eff_process_types_list")
    response = api_client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    data = {x.get("gr") for x in response.data}
    assert len(data) == len(expected)
    for x in expected:
        assert x in data
