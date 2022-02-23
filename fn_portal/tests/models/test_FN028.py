import pytest
from django.db import IntegrityError

from fn_portal.models import FN028
from ..factories import FN011Factory, FN028Factory, GearFactory


def test_FN028_str():
    """Verify that a fishing mode is represented by object type,
    the mode description, the mode code and the project code
    and for the associated project."""

    prj_cd = "LHA_SC11_123"
    mode = "AB"
    mode_des = "trolling"
    project = FN011Factory.build(prj_cd=prj_cd)

    fishing_mode = FN028Factory.build(project=project, mode=mode, mode_des=mode_des)
    shouldbe = "<FishingMode: {} ({}) [{}]>".format(mode_des, mode, prj_cd)

    assert str(fishing_mode) == shouldbe


@pytest.mark.django_db()
def test_duplicate_mode():
    """The mode labels must be unique within project - creating a second
    mode with the same mode value should raise an error."""

    prj_cd = "LHA_IA11_123"
    project = FN011Factory(prj_cd=prj_cd)
    gear = GearFactory()

    mode = "AB"
    mode_des = "trolling"

    mode1 = FN028(project=project, mode=mode, mode_des=mode_des, gear=gear)
    mode1.save()
    mode2 = FN028(project=project, mode=mode, mode_des=mode_des, gear=gear)

    with pytest.raises(IntegrityError) as excinfo:
        mode2.save()

    msg = "duplicate key value violates unique constraint"
    assert msg in str(excinfo.value)
