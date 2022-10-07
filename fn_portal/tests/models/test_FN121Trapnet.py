import pytest
from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121TrapnetFactory


@pytest.mark.django_db
def test_FN121Trapnet_str():
    """
    Verify that the string representation of a FN121Trapnet object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-TRAPNET

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121trapnet = FN121TrapnetFactory(sample=fn121)
    shouldbe = "{}-{}-TRAPNET".format(project_code, sam)
    assert str(fn121trapnet) == shouldbe


@pytest.mark.django_db
def test_FN121Trapnet_fn_keys():
    """Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by
    'trapnet', all separated by a dash:

    e.g. - lha_ia00_123-001-trapnet

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121trapnet = FN121TrapnetFactory(sample=fn121)
    shouldbe = "{}-{}-trapnet".format(project_code, sam)
    assert fn121trapnet.slug == shouldbe.lower()
    assert fn121trapnet.fishnet_keys() == shouldbe.lower()


valid_args = [
    ("lead_angle", 0),
    ("lead_angle", 90),
    ("leaduse", 0),
    ("distoff", 0),
    ("vegetation", 1),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value", valid_args)
def test_FN121Trapnet_parameter_on_bounds(fld, value):
    """Many of the trapnet parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  Many of the most common/likely values are right on the
    bounds of our validators.  This test ensures that we can make sure
    we can save them with distoff=0 for example.
    """

    data = {}
    data[fld] = value

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121trapnet = FN121TrapnetFactory(sample=fn121, **data)
    fn121trapnet.save()


invalid_args = [
    ("lead_angle", -1, "Ensure this value is greater than or equal to 0."),
    ("lead_angle", 91, "Ensure this value is less than or equal to 90."),
    ("leaduse", -1, "Ensure this value is greater than or equal to 0."),
    ("distoff", -1, "Ensure this value is greater than or equal to 0."),
    ("vegetation", 9, "Value 9 is not a valid choice."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121Trapnet_parameter_outside_bounds(fld, value, msg):
    """Many of the trapnet parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121trapnet = FN121TrapnetFactory(sample=fn121, **data)
        fn121trapnet.save()

    assert msg in str(excinfo.value)
