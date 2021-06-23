import pytest
from datetime import datetime
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fn_portal.tests.factories import FN011Factory, LakeFactory, UserFactory


@pytest.fixture
def db_setup():
    """"""
    homer = UserFactory(first_name="Homer", last_name="Simpson")
    bart = UserFactory(first_name="Bart", last_name="Simpson")
    huron = LakeFactory(lake_name="Huron", abbrev="HU")
    superior = LakeFactory(lake_name="Superior", abbrev="SU")

    project1 = FN011Factory(
        prj_cd="LHA_IS00_123",
        prj_nm="Homers Index Project",
        prj_ldr=homer,
        lake=huron,
        prj_date0=datetime(2000, 4, 10),
        prj_date1=datetime(2000, 4, 25),
    )
    project2 = FN011Factory(
        prj_cd="LHA_IS05_999",
        prj_nm="An INDEX project",
        prj_date0=datetime(2005, 10, 10),
        prj_date1=datetime(2005, 10, 15),
    )
    project3 = FN011Factory(
        prj_cd="LSA_IA10_123",
        prj_nm="A Superior InDeX Project",
        prj_date0=datetime(2010, 8, 25),
        prj_date1=datetime(2010, 9, 15),
        lake=superior,
    )
    project4 = FN011Factory(
        prj_cd="LHA_IA02_123",
        prj_nm="A BSM Project",
        prj_date0=datetime(2002, 10, 10),
        prj_date1=datetime(2002, 10, 15),
    )
    project5 = FN011Factory(
        prj_cd="LHA_IA15_002",
        prj_ldr=bart,
        prj_nm="A FWIN",
        prj_date0=datetime(2015, 10, 10),
        prj_date1=datetime(2015, 10, 15),
    )

    return None


@pytest.mark.django_db
def test_can_get_project_list(client, db_setup):
    """Verify that all of our projects appear in our project list."""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 5


@pytest.mark.django_db
def test_can_get_project_detail_404(client, db_setup):
    """If we pass in a project code that does exists, the response should
    be a 404 and nothing should blow-up"""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_cd": "LHA_IA00_ZZZ"})

    assert response.status_code == status.HTTP_200_OK
    returned = response.data
    assert returned["count"] == 0
    assert len(returned["results"]) == 0
    assert returned["next"] is None
    assert returned["previous"] is None


@pytest.mark.django_db
def test_can_get_project_detail(client, db_setup):
    """If we pass in a project code, we should see the corresponding project
    details"""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_cd": "LHA_IS00_123"})
    assert response.status_code == status.HTTP_200_OK

    returned = response.data["results"][0]

    prj_ldr_dict = {
        "username": "simpsonho",
        "first_name": "Homer",
        "last_name": "Simpson",
    }

    assert returned["prj_cd"] == "LHA_IS00_123"
    assert returned["prj_nm"] == "Homers Index Project"
    assert returned["prj_ldr"] == prj_ldr_dict


@pytest.mark.django_db
def test_fn011_year_filter(client, db_setup):
    "verify that we can filter by a single year."

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"year": 2002})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 1
    assert response.data["results"][0].get("prj_cd") == "LHA_IA02_123"


@pytest.mark.django_db
def test_fn011_first_year_filter(client, db_setup):
    """If we pass in just the first year, then all projects after
    that should be returned."""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"year__gte": 2005})
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 3
    returned = [x["prj_cd"] for x in results]

    shouldbe = ["LHA_IS05_999", "LSA_IA10_123", "LHA_IA15_002"]

    for prj in shouldbe:
        assert prj in returned


@pytest.mark.django_db
def test_fn011_last_year_filter(client, db_setup):
    """If we pass in just the last year, then all projects before
    that should be returned."""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"year__lte": 2002})
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 2
    returned = [x["prj_cd"] for x in results]
    shouldbe = ["LHA_IS00_123", "LHA_IA02_123"]
    for prj in shouldbe:
        assert prj in returned


@pytest.mark.django_db
def test_fn011_between_years_filter(client, db_setup):
    """Verify that we can filter projects based on the first and last years
    of a range."""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"year__gte": 2002, "year__lte": 2010})
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 3

    returned = [x["prj_cd"] for x in results]
    shouldbe = ["LHA_IA02_123", "LHA_IS05_999", "LSA_IA10_123"]
    for prj in shouldbe:
        assert prj in returned


@pytest.mark.django_db
def test_fn011_lake_filter(client, db_setup):
    "Verify that we can filter projects based on the lake abbrevation"

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"lake": "SU"})
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == 1
    assert results[0].get("prj_cd") == "LSA_IA10_123"


@pytest.mark.django_db
def test_fn011_project_lead_filter(client, db_setup):
    "Verify that we can filter projects based on the project leads username"
    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_ldr": "simpsonba"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 1
    assert results[0].get("prj_cd") == "LHA_IA15_002"


@pytest.mark.django_db
def test_fn011_project_suffix_filter(client, db_setup):
    "Verify that we can filter projects based on the project suffix"

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"suffix": "999"})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == 1
    assert results[0].get("prj_cd") == "LHA_IS05_999"


project_code_params = ["LHA_IS00_123", "lha_ia00_123", "Lha_Ia00_123"]


@pytest.mark.django_db
@pytest.mark.parametrize("value", project_code_params)
def test_fn011_prj_cd_filter(client, db_setup, value):
    """Verify that we can filter projects based on the project
    code. It should be case insensitive"""

    expected = ["LHA_IS00_123"]

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_cd": value})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == len(expected)
    observed = set([x["prj_cd"] for x in results])
    assert observed == set(expected)


project_code_in_params = (
    [["LHA_IS00_123", "LHA_IS05_999"], ["LHA_IS00_123", "LHA_IS05_999"]],
    # one good, one that does not exsit
    [["LHA_IS00_123", "LHA_IA00_ZZZ"], ["LHA_IS00_123"]],
    # same project code repeated
    [["LHA_IS00_123", "LHA_IS00_123"], ["LHA_IS00_123"]],
    # same project coded repeated in different case
    [["LHA_IS00_123", "lha_ia00_123", "Lha_Ia00_123"], ["LHA_IS00_123"]],
)


@pytest.mark.django_db
@pytest.mark.parametrize("value,expected", project_code_in_params)
def test_fn011_prj_cd_filter(client, db_setup, value, expected):
    """Verify that we can filter projects based on the project
    code. It should be case insensitive"""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_cd": ",".join(value)})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == len(expected)
    observed = set([x["prj_cd"] for x in results])
    assert observed == set(expected)


@pytest.mark.django_db
def test_fn011_prj_cd_like(client, db_setup):
    """Verify that we can filter projects based on part of the project
    code."""

    expected = ["LHA_IS00_123", "LHA_IS05_999"]

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_cd__like": "_IS"})
    assert response.status_code == status.HTTP_200_OK

    results = response.data["results"]
    assert len(results) == len(expected)
    observed = set([x["prj_cd"] for x in results])
    assert observed == set(expected)


project_name_params = ["index", "INDEX", "Index", "iNdEx"]


@pytest.mark.django_db
@pytest.mark.parametrize("value", project_name_params)
def test_fn011_prj_nm_filter(client, db_setup, value):
    """Verify that we can filter projects based on part of the project
    name. It should be case insensitive"""

    expected = ["LHA_IS00_123", "LHA_IS05_999", "LSA_IA10_123"]

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {"prj_nm__like": value})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]

    assert len(results) == len(expected)
    observed = set([x["prj_cd"] for x in results])
    assert observed == set(expected)


project_date_params = (
    ["start_date", "2000-4-10", ["LHA_IS00_123"]],
    ["start_date__lte", "2002-10-10", ["LHA_IS00_123", "LHA_IA02_123"]],
    ["start_date__gte", "2010-8-25", ["LSA_IA10_123", "LHA_IA15_002"]],
    ["end_date", "2000-4-25", ["LHA_IS00_123"]],
    ["end_date__lte", "2002-10-15", ["LHA_IS00_123", "LHA_IA02_123"]],
    ["end_date__gte", "2010-9-15", ["LSA_IA10_123", "LHA_IA15_002"]],
)


@pytest.mark.django_db
@pytest.mark.parametrize("filter,value,expected", project_date_params)
def test_fn011_project_date_filters(client, db_setup, filter, value, expected):
    """There are several fitlers for date attribrutes.  If we apply each
    one, ensure that we get the correct subset of projects back."""

    url = reverse("fn_portal_api:project_list")
    response = client.get(url, {filter: value})
    assert response.status_code == status.HTTP_200_OK
    results = response.data["results"]
    assert len(results) == len(expected)
    observed = set([x["prj_cd"] for x in results])
    assert observed == set(expected)
