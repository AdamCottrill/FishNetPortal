from django.db import IntegrityError
import pytest

from fn_portal.models import FN026
from ..factories import FN011Factory, FN026Factory


def test_FN026_str():
    """Verify that a spatial strata are represented by object type,
    the space description, the space code and the project code
    and for the associated project."""

    prj_cd = "LHA_IA11_123"
    space = "AB"
    space_des = "the river"
    project = FN011Factory.build(prj_cd=prj_cd)

    spatial_strata = FN026Factory.build(
        project=project, space=space, space_des=space_des
    )
    shouldbe = "<Space: {} ({}) [{}]>".format(space_des, space, prj_cd)

    assert str(spatial_strata) == shouldbe


@pytest.mark.django_db()
def test_duplicate_space():
    """The space labels must be unique within project - creating a second
    space with the same space value should raise an error."""

    prj_cd = "LHA_IA11_123"
    space = "AB"
    space_des = "the river"
    project = FN011Factory(prj_cd=prj_cd)

    space1 = FN026(project=project, space=space, space_des=space_des)
    space1.save()
    space2 = FN026(project=project, space=space, space_des=space_des)

    with pytest.raises(IntegrityError) as excinfo:
        space2.save()

    msg = "duplicate key value violates unique constraint"
    assert msg in str(excinfo.value)
