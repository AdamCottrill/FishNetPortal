import pytest
from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121TrawlFactory


@pytest.mark.django_db
def test_FN121Trawl_str():
    """
    Verify that the string representation of a FN121Trawl object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-TRAWL

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121trawl = FN121TrawlFactory(sample=fn121)
    shouldbe = "{}-{}-TRAWL".format(project_code, sam)
    assert str(fn121trawl) == shouldbe


@pytest.mark.django_db
def test_FN121Trawl_fn_keys():
    """Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by
    'trawl', all separated by a dash:

    e.g. - lha_ia00_123-001-trawl

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121trawl = FN121TrawlFactory(sample=fn121)
    shouldbe = "{}-{}-trawl".format(project_code, sam)
    assert fn121trawl.slug == shouldbe.lower()
    assert fn121trawl.fishnet_keys() == shouldbe.lower()


invalid_args = [
    ("vessel_speed", -1, "Ensure this value is greater than or equal to 0."),
    ("vessel_speed", 11, "Ensure this value is less than or equal to 10."),
    ("warp", -1, "Ensure this value is greater than or equal to 0."),
    ("vessel_direction", 11, "Value 11 is not a valid choice."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121Trawl_parameter_outside_bounds(fld, value, msg):
    """Many of the trawl parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121trawl = FN121TrawlFactory(sample=fn121, **data)
        fn121trawl.save()

    assert msg in str(excinfo.value)
