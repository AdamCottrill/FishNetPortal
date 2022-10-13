"""=============================================================
 ~/fn_portal/fn_portal/tests/pydantic_schemas/test_FN121Trawl.py
 Created: 27 May 2022 11:52:44

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121Trawl
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

from fn_portal.data_upload.schemas import FN121Trawl


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-trawl",
        "sample_id": 1,
        "vessel_id": 1,
        "vessel_speed": 4.0,
        "vessel_direction": 4,
        "warp": 11.0,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN121Trawl(**data)

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
        FN121Trawl(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "vessel_speed",
    "vessel_direction",
    "warp",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN121Trawl item is created without error if
    an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN121Trawl(**data)
    assert item.sample_id == data["sample_id"]


alternative_values_list = [
    # field, input, output
    ("vessel_speed", "", None),
    ("vessel_speed", "8.1", 8.1),
    ("vessel_direction", "", None),
    ("warp", "", None),
    ("warp", "10.1", 10.1),
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
    item = FN121Trawl(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    ("vessel_speed", -1.0, "ensure this value is greater than or equal to 0"),
    (
        "vessel_speed",
        10.1,
        "ensure this value is less than or equal to 10",
    ),
    ("warp", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "vessel_direction",
        11,
        "value is not a valid enumeration member;",
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
        FN121Trawl(**data)

    assert msg in str(excinfo.value)
