"""=============================================================
 ~/fn_portal/fn_portal/tests/pydantic_schemas/test_FN121Limno.py
 Created: 27 May 2022 11:52:44

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121Limno
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

from fn_portal.data_upload.schemas import FN121Limno


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-limno",
        "sample_id": 1,
        "do_gear": 12.0,
        "xo2": 11.0,
        "xo22": 11.0,
        "surfdo2": 14.0,
        "surfdo22": 14.0,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN121Limno(**data)

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
        FN121Limno(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "do_gear",
    "xo2",
    "xo22",
    "surfdo2",
    "surfdo22",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN121Limno item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN121Limno(**data)
    assert item.sample_id == data["sample_id"]


mode_list = [
    # field, input, output
    ("do_gear", "", None),
    ("do_gear", "10.1", 10.1),
    ("xo2", "", None),
    ("xo2", "10.1", 10.1),
    ("xo22", "", None),
    ("xo22", "10.1", 10.1),
    ("surfdo2", "", None),
    ("surfdo2", "10.1", 10.1),
    ("surfdo22", "", None),
    ("surfdo22", "10.1", 10.1),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  If the limnology values are strings instead of numbers
    they should be converted to number. If they are empty strings,
    they should be None.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN121Limno(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    ("do_gear", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "do_gear",
        40.6,
        "ensure this value is less than or equal to 20",
    ),
    ("xo2", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "xo2",
        40.6,
        "ensure this value is less than or equal to 20",
    ),
    ("xo22", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "xo22",
        40.6,
        "ensure this value is less than or equal to 20",
    ),
    ("surfdo2", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "surfdo2",
        40.6,
        "ensure this value is less than or equal to 20",
    ),
    ("surfdo22", -40.6, "ensure this value is greater than or equal to 0"),
    (
        "surfdo22",
        40.6,
        "ensure this value is less than or equal to 20",
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
        FN121Limno(**data)

    assert msg in str(excinfo.value)
