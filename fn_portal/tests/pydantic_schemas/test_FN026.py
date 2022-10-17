"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN026.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN026
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
from datetime import datetime

from fn_portal.data_upload.schemas import FN026


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-A1",
        "project_id": 1,
        "space": "A1",
        "space_des": "the lake",
        "space_wt": 0.5,
        # "area_lst": "Foo,bar,baz",
        # "site_lst": "town,city,village",
        # "sitp_lst": "bedrock,sand,gravel,muck",
        "grdep_ge": 10.1,
        "grdep_lt": 100.1,
        "sidep_ge": 10.1,
        "sidep_lt": 100.1,
        "grid_ge": 250.1,
        "grid_lt": 260.1,
        "dd_lat": 45.5,
        "dd_lon": -81.5,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN026(**data)

    assert item.project_id == data["project_id"]
    assert item.slug == data["slug"]
    assert item.space == data["space"].strip().title()
    assert item.space_des == data["space_des"].strip().title()


required_fields = [
    "slug",
    "project_id",
    "space",
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
        FN026(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "space_des",
    "space_wt",
    "grdep_ge",
    "grdep_lt",
    "sidep_ge",
    "sidep_lt",
    "grid_ge",
    "grid_lt",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN026 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN026(**data)
    assert item.project_id == data["project_id"]


space_list = [
    # field, input, output
    ("space", "aa", "AA"),
    ("space", "a1", "A1"),
    ("space", "AA", "AA"),
    ("space", "A1", "A1"),
    ("space", "00", "00"),
    ("space_des", "the bay", "The Bay"),
    ("space_des", "THE BAY", "The Bay"),
    ("space_des", " the bay ", "The Bay"),
    ("grdep_ge", "", None),
    ("grdep_lt", "", None),
    ("sidep_ge", "", None),
    ("sidep_lt", "", None),
    ("grdep_ge", "0", 0),
    ("sidep_ge", "0", 0),
    # strings with just spaces:
    ("grdep_ge", " ", None),
    ("grdep_lt", "  ", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", space_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  For example, Space should be a four letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.  space_des should be trimmed of any
    white space and converted to upper case.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN026(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


paired_field_list = [
    ("dd_lat", "dd_lon", "", None),
    ("dd_lat", "dd_lon", "0", None),
]


@pytest.mark.parametrize("fld1,fld2,value_in,value_out", paired_field_list)
def test_valid_paired_alternatives(data, fld1, fld2, value_in, value_out):
    """When the pydanic model is created, it should transform some
    optional fields.  Some fields must be transformed in pairs - lat
    and long are only valid if they are both populated, or both null.
    Arguments: - `data`:

    """
    data[fld1] = value_in
    data[fld2] = value_in
    item = FN026(**data)
    item_dict = item.dict()
    assert item_dict[fld1] == value_out
    assert item_dict[fld2] == value_out


error_list = [
    (
        "space",
        "AA1",
        "ensure this value has at most 2 characters",
    ),
    (
        "space",
        "A*",
        'string does not match regex "^([A-Z0-9]{2})$"',
    ),
    ("grdep_ge", -3.14, "ensure this value is greater than or equal to 0"),
    ("grdep_lt", -3.14, "ensure this value is greater than 0"),
    ("sidep_ge", -3.14, "ensure this value is greater than or equal to 0"),
    ("sidep_lt", -3.14, "ensure this value is greater than 0"),
    ("grdep_lt", 0, "ensure this value is greater than 0"),
    ("sidep_lt", 0, "ensure this value is greater than 0"),
    (
        "dd_lat",
        None,
        "dd_lat must be populated with a valid latitude if dd_lon is provided",
    ),
    (
        "dd_lon",
        None,
        "dd_lon must be populated with a valid longitude if dd_lat is provided",
    ),
    (
        "dd_lat",
        "0",
        "dd_lat must be populated with a valid latitude if dd_lon is provided",
    ),
    (
        "dd_lon",
        "0",
        "dd_lon must be populated with a valid longitude if dd_lat is provided",
    ),
    (
        "dd_lat",
        40.6,
        "ensure this value is greater than or equal to 41.6",
    ),
    (
        "dd_lat",
        49.5,
        "ensure this value is less than or equal to 49.2",
    ),
    (
        "dd_lon",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon",
        -72.0,
        "ensure this value is less than or equal to -74.32",
    ),
    ("space_wt", 0, "ensure this value is greater than 0"),
    ("space_wt", 1.1, "ensure this value is less than or equal to 1"),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN026(**data)
    assert msg in str(excinfo.value)
