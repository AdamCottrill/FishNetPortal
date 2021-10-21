import pytest


from fn_portal.api.serializers import FN026Serializer

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
        "space": "99",
        "space_des": "Over there",
    }


required_fields = ["project", "space", "space_des"]


@pytest.mark.django_db
@pytest.mark.parametrize("field", required_fields)
def test_required_fields(data, field):
    """

    Arguments:
    - `data`:
    - `field`:
    """
    data[field] = None
    item = FN026Serializer(data=data)
    assert item.is_valid() is False

    message = "This field may not be null."

    assert message in item.errors.get(field)
