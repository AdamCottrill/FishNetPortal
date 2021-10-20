import pytest


from fn_portal.api.serializers import FN022Serializer

# we need to make sure that season are consistent the project year
# and that season end data always occurs on or after season start date:


from ...factories import UserFactory, LakeFactory, FNProtocolFactory, FN011Factory


@pytest.fixture
def fixtures():
    """ """
    LakeFactory(abbrev="HU")
    UserFactory(username="hsimpson")
    FNProtocolFactory(abbrev="FLIN")


@pytest.fixture
def data():
    """ """

    project = FN011Factory(year=2021, prj_cd="LHA_IA21_123")

    return {
        "project": project.slug,
        "ssn": "99",
        "ssn_des": "Season 01",
        "ssn_date0": "2021-09-01",
        "ssn_date1": "2021-10-31",
    }


@pytest.mark.django_db
def test_ssn_date0_equal_to_date1(data):
    """the season dates can be the same - a single day season."""

    data["ssn_date0"] = "2021-10-31"
    item = FN022Serializer(data=data)

    assert item.is_valid() is True


@pytest.mark.django_db
def test_ssn_date1_before_date0(data):
    """An error should be raised if the start date occurs after the end date."""

    data["ssn_date1"] = "2021-05-30"
    item = FN022Serializer(data=data)

    assert item.is_valid() is False

    message = "season end date must occur on or after start date"
    assert message in item.errors.get("ssn_date1")


@pytest.mark.django_db
def test_ssn_date0_inconsistent_with_project_year(data):
    """An error should be raised if the start date is not consistent with
    the year in the project code.

    """
    data["ssn_date0"] = "2020-05-30"
    data["ssn_date1"] = "2020-06-30"
    item = FN022Serializer(data=data)

    assert item.is_valid() is False
    message = "season start year is not constistent with project year."
    assert message in item.errors.get("ssn_date0")
