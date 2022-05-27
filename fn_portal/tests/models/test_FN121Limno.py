import pytest

from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121LimnoFactory


@pytest.mark.django_db
def test_FN121Limno_str():
    """
    Verify that the string representation of a FN121Limno object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-LIMNO

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121limno = FN121LimnoFactory(sample=fn121)
    shouldbe = "{}-{}-LIMNO".format(project_code, sam)
    assert str(fn121limno) == shouldbe


@pytest.mark.django_db
def test_FN121Limno_fn_keys():
    """
    Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by 'limno', all separated by a dash:

    e.g. - lha_ia00_123-001-limno

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121limno = FN121LimnoFactory(sample=fn121)
    shouldbe = "{}-{}-limno".format(project_code, sam)
    assert fn121limno.slug == shouldbe.lower()
    assert fn121limno.fishnet_keys() == shouldbe.lower()


invalid_args = [
    ("do_gear", -10, "Ensure this value is greater than or equal to 0."),
    ("do_gear", 50.1, "Ensure this value is less than or equal to 20."),
    ("xo2", -0.1, "Ensure this value is greater than or equal to 0."),
    ("xo2", 50.1, "Ensure this value is less than or equal to 20."),
    ("xo22", -0.1, "Ensure this value is greater than or equal to 0."),
    ("xo22", 50.1, "Ensure this value is less than or equal to 20."),
    ("surfdo2", -0.1, "Ensure this value is greater than or equal to 0."),
    ("surfdo2", 50.1, "Ensure this value is less than or equal to 20."),
    ("surfdo22", -0.1, "Ensure this value is greater than or equal to 0."),
    ("surfdo22", 50.1, "Ensure this value is less than or equal to 20."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121Limno_parameter_bounds(fld, value, msg):
    """Many of the limno parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121limno = FN121LimnoFactory(sample=fn121, **data)
        fn121limno.save()

    assert msg in str(excinfo.value)
