import pytest

from django.urls import reverse


from fn_portal.models import FN011

from ..fixtures import api_client, users
from ...factories import UserFactory, LakeFactory, FNProtocolFactory, GearFactory


@pytest.fixture
def fixtures():
    """ """
    LakeFactory(abbrev="HU")
    UserFactory(username="Ralph Wiggam")
    FNProtocolFactory(abbrev="FLIN")
    GearFactory(gr_code="GL38")
    GearFactory(gr_code="GL51")
    GearFactory(gr_code="GL64")


@pytest.fixture
def data():
    """
    A complete dicationary with valid, known, data elements that can
    be used in our tests. If it is submitted as is, it should create
    all of the elements of the design tables, it can be compromised in
    known ways to ensure that the validation captures errors and returns appropriated
    error messages.

    """

    data = {
        "fn011": {
            "comment0": "This is a test project. It is going to be awesome.",
            "protocol": "FLIN",
            "lake": "HU",
            "prj_date0": "2021-09-01",
            "prj_date1": "2021-10-31",
            "prj_ldr": "hsimpson",
            "prj_nm": "This is a test project.",
            "prj_cd": "LHA_IA21_123",
        },
        "fn022": [
            {
                "ssn_date0": "2021-09-01",
                "ssn_date1": "2021-09-30",
                "ssn_des": "Early season - september",
                "ssn": "10",
            },
            {
                "ssn_date0": "2021-10-01",
                "ssn_date1": "2021-10-31",
                "ssn_des": "Late season - october",
                "ssn": "20",
            },
        ],
        "fn026": [
            {
                "dd_lat": 44.69195,
                "dd_lon": -80.822,
                "space_des": "East Side",
                "space": "ES",
            },
            {
                "dd_lat": 44.69831,
                "dd_lon": -80.90674,
                "space_des": "West Side",
                "space": "WS",
            },
        ],
        "fn028": [
            {
                "mode": "00",
                "mode_des": "GL38-Across Contours (1)-On Bottom (B)",
                "gear": "GL38",
                "orient": "1",
                "set_type": "b",
            },
            {
                "mode": "10",
                "mode_des": "GL51-Across Contours (1)-On Bottom (B)",
                "gear": "GL51",
                "orient": "1",
                "set_type": "b",
            },
            {
                "mode": "20",
                "mode_des": "GL64-Across Contours (1)-On Bottom (B)",
                "gear": "GL64",
                "orient": "1",
                "set_type": "b",
            },
        ],
        "gear_array": [
            {
                "gear": "GL38",
                "process_types": [{"process_type": "3", "label": "By Panel Group"}],
            },
            {
                "gear": "GL51",
                "process_types": [{"process_type": "3", "label": "By Panel Group"}],
            },
            {
                "gear": "GL64",
                "process_types": [{"process_type": "3", "label": "By Panel Group"}],
            },
        ],
    }
    return data


@pytest.mark.django_db
def test_wizard_good_data(api_client, data, fixtures, users):
    """This is an integration test that ensure the api endpoint that
    consumes the json data from the form wizard successfully create
    the project and all of the associated design tables and returns an
    appropriate 201 Created response.

    """

    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    url = reverse("fn_portal_api:project_wizard")
    response = api_client.post(url, data, format="json")

    from pprint import pprint

    pprint(response.data)

    assert response.status_code == 201

    prj_cd = data["fn011"]["prj_cd"]
    project = FN011.objects.filter(prj_cd=prj_cd).first()

    assert project is not None

    seasons = project.seasons.all()
    assert len(seasons) == 2
    expected = {"Early season - september", "Late season - october"}
    assert {x.ssn_des for x in seasons} == expected

    spaces = project.spatial_strata.all()
    assert len(spaces) == 2
    expected = {"East Side", "West Side"}
    assert {x.space_des for x in spaces} == expected

    modes = project.modes.all()
    assert len(modes) == 3
    expected = {
        "GL38-Across Contours (1)-On Bottom (B)",
        "GL51-Across Contours (1)-On Bottom (B)",
        "GL64-Across Contours (1)-On Bottom (B)",
    }
    assert {x.mode_des for x in modes} == expected

    gears = project.get_gear()
    assert len(gears) == 3
    expected = {
        "GL38",
        "GL51",
        "GL64",
    }
    assert {x.gr_code for x in gears} == expected

    gear_process_types = project.gear_process_types.all()
    assert len(gear_process_types) == 3
    expected = {
        "LHA_IA21_123-GL38-3",
        "LHA_IA21_123-GL51-3",
        "LHA_IA21_123-GL64-3",
    }

    assert {str(x) for x in gear_process_types} == expected


# test duplicate values and descriptions, prj_cd
# unknown lake, protocol, or project lead.
# inconsistent lake and project code
# inconsistent lake and year
# inonsisten start and end dates for project and seasons.
# test overlapping seasons


table_list = [
    ("fn022", "At least one season must be specified"),
    ("fn026", "At least one spatial strata must be specified"),
    ("fn028", "At least one mode must be specified"),
    ("gear_array", "At least one gear and process type must be specified"),
]


@pytest.mark.parametrize("table,message", table_list)
@pytest.mark.django_db()
def test_empty_child_array(api_client, data, fixtures, users, table, message):
    """If any of the arrays associated with the design tables are empty,
    the response should be a 400, with a meaningful error message."""

    data[table] = []

    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    url = reverse("fn_portal_api:project_wizard")
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400

    messages = [x.get(table) for x in response.data]
    assert message in messages

    # make sure nothing was committed to the database:
    prj_cd = data["fn011"]["prj_cd"]
    project = FN011.objects.filter(prj_cd=prj_cd).first()

    assert project is None


fn011_field_list = [
    ("fn011", "prj_cd"),
    ("fn011", "prj_nm"),
    ("fn011", "prj_date0"),
    ("fn011", "prj_date1"),
    ("fn011", "lake"),
    ("fn011", "protocol"),
    # ("fn011", "comment0"),
    ("fn022", "ssn"),
    ("fn022", "ssn_des"),
    ("fn022", "ssn_date0"),
    ("fn022", "ssn_date1"),
    ("fn026", "space"),
    ("fn026", "space_des"),
    # ("fn026", "dd_lat"),
    # ("fn026", "dd_lon"),
    ("fn028", "mode"),
    ("fn028", "mode_des"),
    ("fn028", "gear"),
    ("fn028", "orient"),
    ("fn028", "gruse"),
]


@pytest.mark.parametrize("table,field", fn011_field_list)
@pytest.mark.django_db()
def test_empty_field(api_client, data, fixtures, users, table, field):
    """All of the fields in the FN011 object are required. If any of them
    happen to be empty, the response should be a 400, and include a
    meaningful message.

    """

    prj_cd = data["fn011"]["prj_cd"]

    if table == "fn011":
        data[table][field] = None
    else:
        data[table][0][field] = None

    message = "This field may not be null."

    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    url = reverse("fn_portal_api:project_wizard")
    response = api_client.post(url, data, format="json")
    assert response.status_code == 400

    # the actual error messages are buried deep in the response object:
    messages = [x.get(field) for x in response.data]
    assert message in [x[0] for x in messages]

    # make sure nothing was committed to the database:
    project = FN011.objects.filter(prj_cd=prj_cd).first()

    assert project is None
