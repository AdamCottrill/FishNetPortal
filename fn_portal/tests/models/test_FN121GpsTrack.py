import pytest
from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN121GpsTrackFactory


@pytest.mark.django_db
def test_FN121GpsTrack_str():
    """
    Verify that the string representation of a FN121GpsTrack object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001-GPS_TRACK

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)

    fn121gpstrack = FN121GpsTrackFactory(sample=fn121)
    shouldbe = "{}-{}-{}".format(project_code, sam, fn121gpstrack.track_id)
    assert str(fn121gpstrack) == shouldbe


@pytest.mark.django_db
def test_FN121GpsTrack_fn_keys():
    """Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by
    'gps_track', all separated by a dash:

    e.g. - lha_ia00_123-001-1

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn121gpstrack = FN121GpsTrackFactory(sample=fn121)
    shouldbe = "{}-{}-{}".format(project_code, sam, fn121gpstrack.track_id)
    assert fn121gpstrack.slug == shouldbe.lower()
    assert fn121gpstrack.fishnet_keys() == shouldbe.lower()


invalid_combo_args = [
    (
        "dd_lat",
        45.5,
        "dd_lon",
        None,
        "dd_lon cannot be null if dd_lat is provided.",
    ),
    (
        "dd_lat",
        None,
        "dd_lon",
        -81.5,
        "dd_lat cannot be null if dd_lon is provided.",
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld1,value1,fld2,value2,msg", invalid_combo_args)
def test_wind_speed_direction_clean_method(fld1, value1, fld2, value2, msg):
    """dd_lat and dd_lon must both be populated, or both be
    empty. this test ensure that situation where one is empty and one
    is provided throws the expected error.

    """

    data = {}
    data[fld1] = value1
    data[fld2] = value2

    project = FN011Factory()
    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121gpstrack = FN121GpsTrackFactory(sample=fn121, **data)
        fn121gpstrack.save()

    assert msg in str(excinfo.value)


invalid_args = [
    ("track_id", -1, "Ensure this value is greater than or equal to 0."),
    ("dd_lat", 40.1, "Ensure this value is greater than or equal to 41.7."),
    ("dd_lat", 49.5, "Ensure this value is less than or equal to 49.2."),
    ("dd_lon", -90.0, "Ensure this value is greater than or equal to -89.6."),
    ("dd_lon", -75.0, "Ensure this value is less than or equal to -76.4."),
    ("sidep", -1, "Ensure this value is greater than or equal to 0."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_FN121GpsTrack_parameter_outside_bounds(fld, value, msg):
    """Many of the gps track parameters have min and max validators that
    ensure their values always stay within plausible/reasonable
    limits.  This test ensures that an expected error is thrown if a
    value outside of those bounds is used.

    """

    data = {}
    data[fld] = value

    fn121 = FN121Factory()

    with pytest.raises(ValidationError) as excinfo:
        fn121gpstrack = FN121GpsTrackFactory(sample=fn121, **data)
        fn121gpstrack.save()

    assert msg in str(excinfo.value)
