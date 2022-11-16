import pytest

from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121ElectroFishingFactory


@pytest.mark.django_db
def test_FN121ElectroFishing_str():
    """
    Verify that the string representation of a FN121ElectroFishing object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-ELECTROFISHING

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121electrofishing = FN121ElectroFishingFactory(sample=fn121)
    shouldbe = "{}-{}-ELECTROFISHING".format(project_code, sam)
    assert str(fn121electrofishing) == shouldbe


@pytest.mark.django_db
def test_FN121ElectroFishing_fn_keys():
    """
    Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by 'electrofishing', all separated by a dash:

    e.g. - lha_ia00_123-001-electrofishing

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121electrofishing = FN121ElectroFishingFactory(sample=fn121)
    shouldbe = "{}-{}-electrofishing".format(project_code, sam)
    assert fn121electrofishing.slug == shouldbe.lower()
    assert fn121electrofishing.fishnet_keys() == shouldbe.lower()


invalid_args = [
    ("shock_sec", -10, "Ensure this value is greater than or equal to 0."),
    ("shock_sec", 3001, "Ensure this value is less than or equal to 3000."),
    ("volts_minimum", -10, "Ensure this value is greater than or equal to 0."),
    ("volts_minimum", 1500, "Ensure this value is less than or equal to 1200."),
    ("volts_maximum", -10, "Ensure this value is greater than or equal to 0."),
    ("volts_maximum", 1500, "Ensure this value is less than or equal to 1200."),
    ("volts_mean", -10, "Ensure this value is greater than or equal to 0."),
    ("volts_mean", 1500, "Ensure this value is less than or equal to 1200."),
    ("amps_minimum", -10, "Ensure this value is greater than or equal to 0."),
    ("amps_minimum", 81, "Ensure this value is less than or equal to 80."),
    ("amps_maximum", -10, "Ensure this value is greater than or equal to 0."),
    ("amps_maximum", 81, "Ensure this value is less than or equal to 80."),
    ("amps_mean", -10, "Ensure this value is greater than or equal to 0."),
    ("amps_mean", 81, "Ensure this value is less than or equal to 80."),
    ("power_minimum", -10, "Ensure this value is greater than or equal to 0."),
    ("power_minimum", 15001, "Ensure this value is less than or equal to 15000."),
    ("power_maximum", -10, "Ensure this value is greater than or equal to 0."),
    ("power_maximum", 15001, "Ensure this value is less than or equal to 15000."),
    ("power_mean", -10, "Ensure this value is greater than or equal to 0."),
    ("power_mean", 15001, "Ensure this value is less than or equal to 15000."),
    ("conduct", -0.1, "Ensure this value is greater than or equal to 0."),
    ("conduct", 2000.1, "Ensure this value is less than or equal to 2000."),
    ("turbidity", -0.1, "Ensure this value is greater than or equal to 0."),
    ("turbidity", 400.1, "Ensure this value is less than or equal to 400."),
    ("freq", 0, "Ensure this value is greater than or equal to 10."),
    ("freq", 251, "Ensure this value is less than or equal to 250."),
    ("pulse_dur", -0.1, "Ensure this value is greater than or equal to 0."),
    ("duty_cycle", -0.1, "Ensure this value is greater than or equal to 0."),
    ("duty_cycle", 100.1, "Ensure this value is less than or equal to 100."),
    ("anodes", -1, "Ensure this value is greater than or equal to 1."),
    ("anodes", 5, "Ensure this value is less than or equal to 2."),
    ("num_netters", -1, "Ensure this value is greater than or equal to 0."),
    ("num_netters", 10, "Ensure this value is less than or equal to 8."),
    ("waveform", "WW", "Value 'WW' is not a valid choice."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121ElectroFishing_parameter_bounds(fld, value, msg):
    """Many of the electrofishing parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121electrofishing = FN121ElectroFishingFactory(sample=fn121, **data)
        fn121electrofishing.save()

    assert msg in str(excinfo.value)
