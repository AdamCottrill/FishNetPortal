"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN028.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN028
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
from datetime import time

from fn_portal.data_upload.schemas import FN028


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-A1",
        "gear_id": 1,
        "project_id": 1,
        "mode": "A1",
        "mode_des": "the lake",
        "orient": "1",
        "gruse": 1,
        "effdur_ge": 0.1,
        "effdur_lt": 1.0,
        "efftm0_ge": time(8, 0, 0),
        "efftm0_lt": time(16, 0, 0),
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN028(**data)

    assert item.project_id == data["project_id"]
    assert item.slug == data["slug"]
    assert item.mode == data["mode"].strip().title()
    assert item.mode_des == data["mode_des"].strip().title()


required_fields = [
    "slug",
    "project_id",
    "mode",
    "gear_id",
    "orient",
    "gruse",
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
        FN028(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = ["mode_des", "effdur_ge", "effdur_lt", "efftm0_ge", "efftm0_lt"]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN028 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN028(**data)
    assert item.project_id == data["project_id"]


mode_list = [
    # field, input, output
    ("mode", "aa", "AA"),
    ("mode", "a1", "A1"),
    ("mode", "AA", "AA"),
    ("mode", "A1", "A1"),
    ("mode", "00", "00"),
    (
        "mode_des",
        "Bottom Set Gill Nets Accross Contours",
        "Bottom Set Gill Nets Accross Contours",
    ),
    (
        "mode_des",
        "BOTTOM SET GILL NETS ACCROSS CONTOURS",
        "Bottom Set Gill Nets Accross Contours",
    ),
    (
        "mode_des",
        "bottom set gill nets accross contours",
        "Bottom Set Gill Nets Accross Contours",
    ),
    (
        "mode_des",
        None,
        "Not Specified",
    ),
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
    item = FN028(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "mode",
        "AA1",
        "ensure this value has at most 2 characters",
    ),
    (
        "mode",
        "A*",
        'string does not match regex "^([A-Z0-9]{2})$"',
    ),
    ("effdur_ge", -3.14, "ensure this value is greater than 0"),
    ("effdur_lt", -3.14, "ensure this value is greater than 0"),
    ("effdur_ge", 0, "ensure this value is greater than 0"),
    ("effdur_lt", 0, "ensure this value is greater than 0"),
    (
        "efftm0_lt",
        time(6, 0, 0),
        "Latest set time (efftm0_lt=06:00:00) is earlier than earliest set time(efftm0_ge=08:00:00)",
    ),
    (
        "efftm0_ge",
        "foo",
        "invalid time format",
    ),
    (
        "efftm0_lt",
        "foo",
        "invalid time format",
    ),
    (
        "orient",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "gruse",
        99,
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
        FN028(**data)

    assert msg in str(excinfo.value)
