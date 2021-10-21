import pytest

from random import randint

from fn_portal.api.serializers import FN028Serializer

from ...factories import (
    UserFactory,
    LakeFactory,
    FNProtocolFactory,
    FN011Factory,
    GearFactory,
)


@pytest.fixture
def data():
    """ """

    project = FN011Factory(year=2021, prj_cd="LHA_IA21_123")
    gear = GearFactory(gr_code="GL38")

    return {
        "project": project.slug,
        "gear": gear,
        "mode": "99",
        "mode_des": "Over there",
        "orient": 1,
        "gruse": 1,
    }


required_fields = ["project", "gear", "mode", "mode_des", "orient", "gruse"]


@pytest.mark.django_db
@pytest.mark.parametrize("field", required_fields)
def test_required_fields(data, field):
    """

    Arguments:
    - `data`:
    - `field`:
    """
    data[field] = None
    item = FN028Serializer(data=data)
    assert item.is_valid() is False
    message = "This field may not be null."
    assert message in item.errors.get(field)


fk_field_list = ["orient", "gruse"]


@pytest.mark.django_db
@pytest.mark.parametrize("field", fk_field_list)
def test_invalid_choices(data, field):
    """orient and gr use are choice fields. If we recieve an invalid
    choice, the serializer should be invalid and raise an appropriate
    error message.

    """

    data[field] = "zz"
    item = FN028Serializer(data=data)
    assert item.is_valid() is False

    message = '"zz" is not a valid choice.'
    assert message in item.errors.get(field)


fk_field_list = ["project", "gear"]


@pytest.mark.django_db
@pytest.mark.parametrize("field", fk_field_list)
def test_unknown_related_object(data, field):
    """The fn028 serializer has related field for project and gear.
    If a pk is provied that is not know to exists, it will not be
    valid and should raise an error.

    """

    pk = randint(1000, 10000)
    data[field] = pk
    item = FN028Serializer(data=data)
    assert item.is_valid() is False

    message = f'Invalid pk "{pk}" - object does not exist.'
    assert message in item.errors.get(field)
