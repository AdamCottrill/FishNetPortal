"""=============================================================
 ~/fn_portal/fn_portal/tests/pydantic_schemas/test_FN121Electrofishing.py
 Created: 27 May 2022 11:52:44

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121Electrofishing
  objects validate as expected.

  The script includes:

  1.  a dictionary that representes complete, valid data.

  2. a list of fields and associated modifications that should be
     automatically tranformed by Pydantic (e.g. trimming whitespaces
     and converting to title case)

  3. a list of required fields that are systematically omitted,

  4. and finally a list of changes to the dictionary of good data that
     invalidates it in a known way and verifies that pydantic raises
     the expected exception.

 A. Cottrill
=============================================================

"""


import pytest
from pydantic import ValidationError

from fn_portal.data_upload.schemas import FN121ElectroFishingFactory


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-limno",
        "sample_id": 1,
        "shock_sec": 600,
        "volts_mean": 120,
        "freq": 60,
        "duty_cycle": 90,
        "waveform": "PDC",
        "anodes": 1,
        "num_netters": 3,
    }
    return data


@pytest.fixture
def choices():

    waveforms = {
        "Smooth DC": "SDC",
        "Pulsed DC": "PDC",
        "Burst of Pulses DC": "BPDC",
        "Alternating Current (AC)": "AC",
        "Pulsed AC": "PAC",
        "Rectangular Wave DC": "RDC",
        "Rectangular Wave Burst DC": "RBDC",
    }

    return {"waveform_choices": waveforms}


def test_valid_data(data, choices):
    """

    Arguments:
    - `data`:
    """

    FN121ElectroFishing = FN121ElectroFishingFactory(**choices)
    item = FN121ElectroFishing(**data)

    assert item.sample_id == data["sample_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "sample_id",
]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, choices, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    FN121ElectroFishing = FN121ElectroFishingFactory(**choices)

    with pytest.raises(ValidationError) as excinfo:
        FN121ElectroFishing(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "volts_min",
    "volts_max",
    "volts_mean",
    "amps_min",
    "amps_max",
    "amps_mean",
    "power_min",
    "power_max",
    "power_mean",
    "conduct",
    "turbidity",
    "pulse_dur",
    "duty_cycle",
    "shock_sec",
    "freq",
    "anodes",
    "num_netters",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, choices, fld):
    """Verify that the FN121ElectroFishing item is created without
    error if an optional field is omitted

    Arguments:
    - `data`:

    """
    FN121ElectroFishing = FN121ElectroFishingFactory(**choices)

    data[fld] = None
    item = FN121ElectroFishing(**data)
    assert item.sample_id == data["sample_id"]


mode_list = [
    # field, input, output
    ("volts_mean", "", None),
    ("volts_mean", "10.1", 10.1),
    ("amps_mean", "", None),
    ("amps_mean", "10.1", 10.1),
    ("power_mean", "", None),
    ("power_mean", "10.1", 10.1),
    ("conduct", "", None),
    ("conduct", "10.1", 10.1),
    ("turbidity", "", None),
    ("turbidity", "10.1", 10.1),
    ("pulse_dur", "", None),
    ("pulse_dur", "10.1", 10.1),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, choices, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  If the limnology values are strings instead of numbers
    they should be converted to number. If they are empty strings,
    they should be None.

    Arguments:
    - `data`:

    """

    FN121ElectroFishing = FN121ElectroFishingFactory(**choices)
    data[fld] = value_in
    item = FN121ElectroFishing(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    ("volts_min", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "volts_min",
        1201,
        "ensure this value is less than or equal to 1200",
    ),
    ("volts_max", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "volts_max",
        1201,
        "ensure this value is less than or equal to 1200",
    ),
    ("volts_mean", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "volts_mean",
        1201,
        "ensure this value is less than or equal to 1200",
    ),
    ("amps_min", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "amps_min",
        81,
        "ensure this value is less than or equal to 80",
    ),
    ("amps_max", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "amps_max",
        81,
        "ensure this value is less than or equal to 80",
    ),
    ("amps_mean", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "amps_mean",
        80.1,
        "ensure this value is less than or equal to 80",
    ),
    ("power_min", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "power_min",
        15001,
        "ensure this value is less than or equal to 15000",
    ),
    ("power_max", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "power_max",
        15001,
        "ensure this value is less than or equal to 15000",
    ),
    ("power_mean", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "power_mean",
        15001,
        "ensure this value is less than or equal to 15000",
    ),
    ("conduct", -1, "ensure this value is greater than or equal to 0"),
    (
        "conduct",
        2000.1,
        "ensure this value is less than or equal to 2000",
    ),
    ("turbidity", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "turbidity",
        400.1,
        "ensure this value is less than or equal to 400",
    ),
    ("freq", 1, "ensure this value is greater than or equal to 10"),
    (
        "freq",
        251,
        "ensure this value is less than or equal to 250",
    ),
    ("pulse_dur", -1, "ensure this value is greater than or equal to 0"),
    ("duty_cycle", -0.1, "ensure this value is greater than or equal to 0"),
    (
        "duty_cycle",
        100.1,
        "ensure this value is less than or equal to 100",
    ),
    ("waveform", "AA", "value is not a valid enumeration member"),
    ("anodes", 0, "ensure this value is greater than or equal to 1"),
    (
        "anodes",
        10,
        "ensure this value is less than or equal to 2",
    ),
    ("num_netters", -1, "ensure this value is greater than or equal to 0"),
    (
        "num_netters",
        10,
        "ensure this value is less than or equal to 8",
    ),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, choices, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    FN121ElectroFishing = FN121ElectroFishingFactory(**choices)

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN121ElectroFishing(**data)

    assert msg in str(excinfo.value)
