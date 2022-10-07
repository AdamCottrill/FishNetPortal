import pytest
from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121WeatherFactory


@pytest.mark.django_db
def test_FN121Weather_str():
    """
    Verify that the string representation of a FN121Weather object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-WEATHER

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121weather = FN121WeatherFactory(sample=fn121)
    shouldbe = "{}-{}-WEATHER".format(project_code, sam)
    assert str(fn121weather) == shouldbe


@pytest.mark.django_db
def test_FN121Weather_fn_keys():
    """Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by
    'weather', all separated by a dash:

    e.g. - lha_ia00_123-001-weather

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121weather = FN121WeatherFactory(sample=fn121)
    shouldbe = "{}-{}-weather".format(project_code, sam)
    assert fn121weather.slug == shouldbe.lower()
    assert fn121weather.fishnet_keys() == shouldbe.lower()


@pytest.mark.django_db
def test_xweather_propery():
    """The xweather property is a concatenated string comprised of the
    precip duration followd by the wave_duration."""

    project = FN011Factory()
    fn121 = FN121Factory()
    fn121weather = FN121WeatherFactory(sample=fn121, precip_duration=2, wave_duration=3)
    assert fn121weather.xweather == "23"


wind_args = [
    (0, 0, "000"),
    (90, 25, "090-25"),
    (180, 10, "180-10"),
    (270, 15, "270-15"),
    (360, 5, "360-05"),
]


@pytest.mark.django_db
@pytest.mark.parametrize("wind_direction,wind_speed, expected", wind_args)
def test_wind0_property(wind_direction, wind_speed, expected):
    """Wind is actually a compostite string made up of the
    wind_direction0, followed by the wind_speed0 separated by a
    hyphen.  Using the examples from the data dictinary, verify that
    the combinations of speed and wind direction produce the
    appropriate wind0 string.

    """
    project = FN011Factory()
    fn121 = FN121Factory()
    fn121weather = FN121WeatherFactory(
        sample=fn121, wind_direction0=wind_direction, wind_speed0=wind_speed
    )

    assert fn121weather.wind0 == expected


@pytest.mark.django_db
@pytest.mark.parametrize("wind_direction,wind_speed, expected", wind_args)
def test_wind1_property(wind_direction, wind_speed, expected):
    """Wind is actually a compostite string made up of the
    wind_direction1, followed by the wind_speed1 separated by a
    hyphen.  Using the examples from the data dictinary, verify that
    the combinations of speed and wind direction produce the
    appropriate wind1 string.

    """
    project = FN011Factory()
    fn121 = FN121Factory()
    fn121weather = FN121WeatherFactory(
        sample=fn121, wind_direction1=wind_direction, wind_speed1=wind_speed
    )
    assert fn121weather.wind1 == expected


invalid_combo_args = [
    (
        "wave_duration",
        1,
        "precip_duration",
        None,
        "precip_duration cannot be null if wave_duration is provided.",
    ),
    (
        "wave_duration",
        None,
        "precip_duration",
        1,
        "wave_duration cannot be null if precip_duration is provided.",
    ),
    (
        "wind_speed0",
        0,
        "wind_direction0",
        90,
        "wind_direction0 and wind_speed0 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed0",
        10,
        "wind_direction0",
        0,
        "wind_direction0 and wind_speed0 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed0",
        None,
        "wind_direction0",
        0,
        "wind_direction0 and wind_speed0 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed0",
        0,
        "wind_direction0",
        None,
        "wind_direction0 and wind_speed0 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed0",
        10,
        "wind_direction0",
        None,
        "wind_direction0 cannot be null if wind_speed0 is provided.",
    ),
    (
        "wind_speed0",
        None,
        "wind_direction0",
        10,
        "wind_speed0 cannot be null if wind_direction0 is provided.",
    ),
    (
        "wind_speed1",
        0,
        "wind_direction1",
        90,
        "wind_direction1 and wind_speed1 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed1",
        10,
        "wind_direction1",
        0,
        "wind_direction1 and wind_speed1 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed1",
        None,
        "wind_direction1",
        0,
        "wind_direction1 and wind_speed1 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed1",
        0,
        "wind_direction1",
        None,
        "wind_direction1 and wind_speed1 must both be 0 if one of them is 0.",
    ),
    (
        "wind_speed1",
        10,
        "wind_direction1",
        None,
        "wind_direction1 cannot be null if wind_speed1 is provided.",
    ),
    (
        "wind_speed1",
        None,
        "wind_direction1",
        10,
        "wind_speed1 cannot be null if wind_direction1 is provided.",
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld1,value1,fld2,value2,msg", invalid_combo_args)
def test_wind_speed_direction_clean_method(fld1, value1, fld2, value2, msg):
    """The wind speed and direction fields are complictated. They both
    have to populated, and they can only be 0 if they are both 0.
    Verify that the correct error is raised if we try so save a record
    eith one of the fields blank or ueqal to 0.

    """

    data = {}
    data[fld1] = value1
    data[fld2] = value2

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121weather = FN121WeatherFactory(sample=fn121, **data)
        fn121weather.save()

    assert msg in str(excinfo.value)


invalid_args = [
    ("airtem0", -40, "Ensure this value is greater than or equal to -30."),
    ("airtem0", 50.1, "Ensure this value is less than or equal to 45."),
    ("airtem1", -40, "Ensure this value is greater than or equal to -30."),
    ("airtem1", 50.1, "Ensure this value is less than or equal to 45."),
    ("wind_speed0", -1, "Ensure this value is greater than or equal to 0."),
    ("wind_speed0", 101, "Ensure this value is less than or equal to 100."),
    ("wind_speed1", -1, "Ensure this value is greater than or equal to 0."),
    ("wind_speed1", 101, "Ensure this value is less than or equal to 100."),
    ("wind_direction0", -1, "Ensure this value is greater than or equal to 0."),
    ("wind_direction0", 361, "Ensure this value is less than or equal to 360."),
    ("wind_direction1", -1, "Ensure this value is greater than or equal to 0."),
    ("wind_direction1", 361, "Ensure this value is less than or equal to 360."),
    ("cloud_pc0", -0.1, "Ensure this value is greater than or equal to 0."),
    ("cloud_pc0", 100.1, "Ensure this value is less than or equal to 100."),
    ("cloud_pc1", -0.1, "Ensure this value is greater than or equal to 0."),
    ("cloud_pc1", 100.1, "Ensure this value is less than or equal to 100."),
    ("waveht0", -0.1, "Ensure this value is greater than or equal to 0."),
    ("waveht0", 3.1, "Ensure this value is less than or equal to 3."),
    ("waveht1", -0.1, "Ensure this value is greater than or equal to 0."),
    ("waveht1", 3.1, "Ensure this value is less than or equal to 3."),
    # choice fields
    ("precip0", "ZZ", "Value 'ZZ' is not a valid choice."),
    ("precip1", "ZZ", "Value 'ZZ' is not a valid choice."),
    ("wave_duration", 9, "Value 9 is not a valid choice."),
    ("precip_duration", 9, "Value 9 is not a valid choice."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121Weather_parameter_bounds(fld, value, msg):
    """Many of the weather parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121weather = FN121WeatherFactory(sample=fn121, **data)
        fn121weather.save()

    assert msg in str(excinfo.value)
