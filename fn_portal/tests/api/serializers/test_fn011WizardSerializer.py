from fn_portal.api.serializers import FN011WizardSerializer

import pytest
from ...factories import UserFactory, LakeFactory, FNProtocolFactory


@pytest.fixture
def fixtures():
    """ """
    LakeFactory(abbrev="HU")
    UserFactory(username="hsimpson")
    FNProtocolFactory(abbrev="FLIN")


@pytest.fixture
def data():
    """ """

    return {
        "comment0": "This is a test project. It is going to be awesome.",
        "protocol": "FLIN",
        "lake": "HU",
        "prj_date1": "2021-10-31",
        "prj_date0": "2021-09-01",
        "prj_ldr": "hsimpson",
        "prj_nm": "This is a test project.",
        "prj_cd": "LHA_IA21_123",
    }


#        """ensure that the project code is a valid FN-II project code"""
#
#        + start date occurs on or before end date,
#        + start date and end date are in the same calendar year, and
#        + that year in both dates agree with the year in prj_cd
#        + project code siffux matches lake


field_values = [
    ("prj_date1", "2021-05-31", "project end date must occur on or after start date"),
    (
        "prj_cd",
        "LSA_IA21_123",
        "project code suffix (LSA) is not consistent with selected lake (HU).",
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("field,value,message", field_values)
def test_switched_dates(fixtures, data, field, value, message):
    """an error should be raised if start date occured after the end date."""

    data[field] = value
    item = FN011WizardSerializer(data=data)
    assert item.is_valid() is False

    assert message in item.errors.get(field)


@pytest.mark.django_db
def test_start_end_year(fixtures, data):
    """An error should be thrown if the start and end data occur in
    different years.

    """
    message = "project start and end occur in different years"
    data["prj_date0"] = "2020-05-31"
    item = FN011WizardSerializer(data=data)
    assert item.is_valid() is False
    assert message in item.errors["prj_date1"][0]


@pytest.mark.django_db
def test_wrong_start_year(fixtures, data):
    """An error should be raised if year of the start date is not
    consistent with the project code.

    """

    data["prj_cd"] = "LHA_IA10_200"

    item = FN011WizardSerializer(data=data)
    assert item.is_valid() is False
    message = "year of project start is not consistent with year in project code."
    assert message in item.errors["prj_date0"][0]


valid_prj_cds = [
    "LHA_IA21_708",
    "LHA_IA21_712",
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd", valid_prj_cds)
def test_valid_prj_cds(fixtures, data, prj_cd):
    """The serialtizer should be valid if we pass in a valid FN-II prj_cd."""

    data["prj_cd"] = prj_cd
    item = FN011WizardSerializer(data=data)

    assert item.is_valid() is True


invalid_prj_cds = [
    "LHA_IA21_CINN",
    "LHA_IA21708",
    "LHA_IA21__12",
    "LHAIA221_0092",
    "LHA_ia21_001",
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd", invalid_prj_cds)
def test_invalid_prj_cds(fixtures, data, prj_cd):
    """The serializer should raise an error if we pass in an invalid FN-II prj_cd"""

    data["prj_cd"] = prj_cd
    item = FN011WizardSerializer(data=data)
    assert item.is_valid() is False

    message = "That is not a valid FN-II project code."
    from pprint import pprint

    pprint(item.errors)
    assert message in item.errors["prj_cd"][0]
