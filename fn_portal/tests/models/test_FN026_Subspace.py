from django.db import IntegrityError
import pytest

from fn_portal.models import FN026Subspace
from ..factories import FN011Factory, FN026Factory, FN026SubspaceFactory


@pytest.mark.django_db()
def test_FN026Subspace_slug_on_save():
    """When we save an FN026Subspace object it slug should be
    populated with a string that is made up of the project code, the
    space, and the subspace codes, all separated with dashes.
    e.g. - 'lha_ia99_123-aa-01'
    """

    prj_cd = "LHA_IA99_123"
    space_code = "AA"
    subspace_code = "01"

    shouldbe = "{}-{}-{}".format(prj_cd, space_code, subspace_code)

    project = FN011Factory(prj_cd=prj_cd)

    space = FN026Factory(project=project, space=space_code)

    subspace = FN026SubspaceFactory.build(space=space, subspace=subspace_code)
    subspace.save()
    assert subspace.slug == shouldbe.lower()


@pytest.mark.django_db()
def test_FN026Subspace_str():
    """Verify that the string representation of a subspatial contains
    the object type ('Subspace') the subspace description, the space
    and subspace codes and the project code and for the associated
    project.

    e.g. = '<Subspace: the lower river (AB-01) [LHA_IA11_123]>'

    """

    prj_cd = "LHA_IA11_123"
    space_code = "AB"
    subspace_code = "01"
    subspace_des = "the lower river"

    project = FN011Factory.build(prj_cd=prj_cd)

    space = FN026Factory.build(project=project, space=space_code)

    subspace = FN026SubspaceFactory.build(
        space=space, subspace=subspace_code, subspace_des=subspace_des
    )

    shouldbe = "<Subspace: {} ({}-{}) [{}]>".format(
        subspace_des, space_code, subspace_code, prj_cd
    )

    assert str(subspace) == shouldbe


@pytest.mark.django_db()
def test_FN026Subspace_label_property():
    """The FN026Subspace model has a label property that should return
    a concatenation of the space and space desc. Label is a convience
    property used for label data points, charts and maps.

    e.g. = '01-Lower River'

    """

    subspace_code = "01"
    subspace_des = "the lower river"

    subspace = FN026SubspaceFactory(subspace=subspace_code, subspace_des=subspace_des)

    shouldbe = "{}-{}".format(subspace_code, subspace_des.title())
    assert subspace.label == shouldbe


duplicate_codes = [
    (
        "01",
        "the upper river",
        "01",
        "the lower river",
    ),
    (
        "01",
        "the upper river",
        "02",
        "the upper river",
    ),
]


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "subspace_code1,subspace_des1,subspace_code2,subspace_des2", duplicate_codes
)
def test_duplicate_subspace_within_space(
    subspace_code1, subspace_des1, subspace_code2, subspace_des2
):
    """The space descriptions and codes must be unique within a space -
    creating a second subspace within space with the same subspace
    code or des should raise an unique constrain error.  This
    constraint is enforced at the databse level.
    """

    prj_cd = "LHA_IA11_123"
    project = FN011Factory(prj_cd=prj_cd)

    space_code = "AB"
    space_des = "the river"
    space = FN026Factory(project=project, space=space_code, space_des=space_des)

    # this one will work
    subspace = FN026Subspace(
        space=space, subspace=subspace_code1, subspace_des=subspace_des1
    )
    subspace.save()

    # this one  should throw an error when we save it.
    subspace2 = FN026Subspace(
        space=space, subspace=subspace_code2, subspace_des=subspace_des2
    )

    with pytest.raises(IntegrityError) as excinfo:
        subspace2.save()

    msg = "subspace or subspace_des values already exist in this space"
    assert msg in str(excinfo.value)


@pytest.mark.django_db()
@pytest.mark.parametrize(
    "subspace_code1,subspace_des1,subspace_code2,subspace_des2", duplicate_codes
)
def test_duplicate_subspace_within_project(
    subspace_code1, subspace_des1, subspace_code2, subspace_des2
):

    """The space desciptions and codes must be unique within a project -
    creating a second subspace with a subspace code or desciption that
    already exists in our project should raise an unique constrain
    error.  This is enforced by our model's save/clean methods.

    """

    prj_cd = "LHA_IA11_123"
    project = FN011Factory(prj_cd=prj_cd)

    space_code = "AB"
    space_des = "the river"
    space = FN026Factory(project=project, space=space_code, space_des=space_des)

    # this one will work
    subspace = FN026Subspace(
        space=space, subspace=subspace_code1, subspace_des=subspace_des1
    )
    subspace.save()

    # different space:
    space_code = "XY"
    space_des = "the lake"
    space2 = FN026Factory(project=project, space=space_code, space_des=space_des)

    # this one  should throw an error when we save it:
    subspace2 = FN026Subspace(
        space=space2, subspace=subspace_code2, subspace_des=subspace_des2
    )

    with pytest.raises(IntegrityError) as excinfo:
        subspace2.save()

    msg = "subspace or subspace_des values already exist in this project"
    assert msg in str(excinfo.value)


@pytest.mark.skip
@pytest.mark.django_db()
def test_subspace_points_within_space_polygon():
    """If space has a polygon geometry, verify that the lat-lon for
    out subspace is completely within it."""
    assert 0 == 1


@pytest.mark.skip
@pytest.mark.django_db()
def test_duplicate_subspace_polygon_within_space_geom():
    """If space has a polygon geometry, and our subspace is a polygon,
    verify that the subspace geometry is completely contained
    within the space geometry.

    """
    assert 0 == 1


@pytest.mark.skip
@pytest.mark.django_db()
def test_subspace_polygons_are_disjoint():
    """If we have more than one subspace in a spatial strata, we
    need to ensure that they don't overlap.

    """
    assert 0 == 1
