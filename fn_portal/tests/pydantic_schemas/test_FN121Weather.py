"""=============================================================
 ~/fn_portal/fn_portal/tests/pydantic_schemas/test_FN121Weather.py
 Created: 27 May 2022 11:52:44

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121Weather
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

from fn_portal.data_upload.schemas import FN121Weather


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-trawl",
        "sample_id": 1,
        "airtem0": 5.0,
        "airtem1": 9.1,
        "cloud_pc0": 10,
        "cloud_pc1": 85,
        "waveht0": 0.3,
        "waveht1": 0.1,
        "precip0": "10",
        "precip1": "40",
        "wind0": "270-15",
        "wind1": "090-10",
        "xweather": "14",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN121Weather(**data)

    assert item.sample_id == data["sample_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "sample_id",
]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN121Weather(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "airtem0",
    "airtem1",
    "cloud_pc0",
    "cloud_pc1",
    "waveht0",
    "waveht1",
    "precip0",
    "precip1",
    "wind0",
    "wind1",
    "xweather",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN121Weather item is created without error if
    an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN121Weather(**data)
    assert item.sample_id == data["sample_id"]


alternative_values_list = [
    # field, input, output
    ("airtem0", "", None),
    ("airtem0", "8.1", 8.1),
    ("airtem1", "", None),
    ("airtem1", "8.1", 8.1),
    ("cloud_pc0", "", None),
    ("cloud_pc0", "10", 10),
    ("cloud_pc1", "", None),
    ("cloud_pc1", "10", 10),
    ("waveht0", "", None),
    ("waveht0", "2.1", 2.1),
    ("waveht1", "", None),
    ("waveht1", "2.1", 2.1),
    ("wind0", "000-00", "000-00"),
    ("wind1", "000-00", "000-00"),
    # wind speed doesn't have to be left padded:
    ("wind0", "270-5", "270-5"),
    ("wind1", "100-9", "100-9"),
]


@pytest.mark.parametrize("fld,value_in,value_out", alternative_values_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  If the trawl values are strings instead of numbers
    they should be converted to number. If they are empty strings,
    they should be None.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN121Weather(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    ("airtem0", -31.0, "ensure this value is greater than or equal to -30"),
    (
        "airtem0",
        45.1,
        "ensure this value is less than or equal to 45",
    ),
    ("airtem1", -31.0, "ensure this value is greater than or equal to -30"),
    (
        "airtem1",
        45.1,
        "ensure this value is less than or equal to 45",
    ),
    ("cloud_pc0", -1.0, "ensure this value is greater than or equal to 0"),
    (
        "cloud_pc0",
        100.1,
        "ensure this value is less than or equal to 100",
    ),
    ("cloud_pc1", -1.0, "ensure this value is greater than or equal to 0"),
    (
        "cloud_pc1",
        100.1,
        "ensure this value is less than or equal to 100",
    ),
    ("waveht0", -1.0, "ensure this value is greater than or equal to 0"),
    (
        "waveht0",
        3.6,
        "ensure this value is less than or equal to 3.5",
    ),
    ("waveht1", -1.0, "ensure this value is greater than or equal to 0"),
    (
        "waveht1",
        3.6,
        "ensure this value is less than or equal to 3.5",
    ),
    (
        "precip0",
        "11",
        "value is not a valid enumeration member;",
    ),
    (
        "precip1",
        "11",
        "value is not a valid enumeration member;",
    ),
    (
        "wind0",
        "0",
        "string does not match regex",
    ),
    (
        "wind1",
        "0",
        "string does not match regex",
    ),
    (
        "xweather",
        "0",
        "string does not match regex",
    ),
    (
        "xweather",
        "99",
        "string does not match regex",
    ),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN121Weather(**data)

    assert msg in str(excinfo.value)
