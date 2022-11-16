"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN122.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN122
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
from datetime import time
from pydantic import ValidationError

from fn_portal.data_upload.schemas import FN122


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001",
        "sample_id": 1,
        "eff": "001",
        "effdst": 75,
        "grdep0": 12,
        "grdep1": 12.5,
        "grtem0": 12.2,
        "grtem1": 13.1,
        "waterhaul": False,
        "comment2": "best effort yet",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN122(**data)

    assert item.sample_id == data["sample_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "sample_id",
    "eff",
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
        FN122(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "effdst",
    "grdep0",
    "grdep1",
    "grtem0",
    "grtem1",
    "comment2",
    "waterhaul",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN122 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN122(**data)
    assert item.sample_id == data["sample_id"]


mode_list = [
    # field, input, output
    ("eff", "abc", "ABC"),
    ("effdst", "", None),
    ("grdep0", "", None),
    ("grdep1", "", None),
    ("grtem0", "", None),
    ("grtem1", "", None),
    ("eff", "1", "1"),
    ("eff", "12", "12"),
    ("eff", "2 ", "2"),
    ("eff", " 2", "2"),
    ("waterhaul", None, False),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  Mode should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.  mode_des should be trimmed of any
    white mode and converted to upper case.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN122(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "effdst",
        -40.6,
        "ensure this value is greater than 0",
    ),
    (
        "grdep0",
        -40.6,
        "ensure this value is greater than 0",
    ),
    (
        "grdep1",
        -40.6,
        "ensure this value is greater than 0",
    ),
    (
        "grtem0",
        -31.6,
        "ensure this value is greater than or equal to -30",
    ),
    (
        "grtem1",
        -31.6,
        "ensure this value is greater than or equal to -30",
    ),
    (
        "grtem0",
        31.6,
        "ensure this value is less than or equal to 30",
    ),
    (
        "grtem1",
        31.6,
        "ensure this value is less than or equal to 30",
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
        FN122(**data)

    assert msg in str(excinfo.value)
