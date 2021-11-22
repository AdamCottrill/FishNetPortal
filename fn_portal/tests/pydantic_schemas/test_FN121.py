"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN028.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN121
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
from datetime import datetime, time

from fn_portal.data_upload.schemas import FN121


@pytest.fixture()
def data():
    data = {
        "grid5_id": 1,
        "project_id": 1,
        "ssn_id": 1,
        "space_id": 1,
        "mode_id": 1,
        "slug": "lha_ia19_022-12",
        "sam": "12",
        "effdt0": datetime(2019, 8, 2),
        "efftm0": time(8, 0, 0),
        "effdt1": datetime(2019, 8, 3),
        "efftm1": time(8, 0, 0),
        "effdur": 24.0,
        "effst": 1,
        "sitp": None,
        "site": "the dock",
        "dd_lat": 45.5,
        "dd_lon": -81.2,
        "dd_lat1": 45.6,
        "dd_lon1": -81.1,
        "sitem": 18.1,
        "sitem0": 18.1,
        "sitem1": 21.2,
        "sidep": 10.2,
        "grdepmin": 8.2,
        "grdepmax": 11.6,
        "secchi": None,
        "xslime": None,
        "crew": "homer",
        "comment1": "not a real sample",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN121(**data)

    assert item.project_id == data["project_id"]
    assert item.slug == data["slug"]


required_fields = [
    "grid5_id",
    "project_id",
    "ssn_id",
    "space_id",
    "mode_id",
    "slug",
    "sam",
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
        FN121(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "effdt0",
    "efftm0",
    "effdt1",
    "efftm1",
    "effdur",
    "effst",
    "sitp",
    "site",
    "dd_lat",
    "dd_lon",
    "dd_lat1",
    "dd_lon1",
    "sitem",
    "sitem0",
    "sitem1",
    "sidep",
    "grdepmin",
    "grdepmax",
    "secchi",
    "xslime",
    "crew",
    "comment1",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN121 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN121(**data)
    assert item.project_id == data["project_id"]


mode_list = [
    # field, input, output
    ("effdur", "", None),
    ("sidep", "", None),
    ("secchi", "", None),
    ("grdepmin", "", None),
    ("grdepmax", "", None),
    ("sitem", "", None),
    ("sitem0", "", None),
    ("sitem1", "", None),
    ("dd_lat", "", None),
    ("dd_lon", "", None),
    ("dd_lat1", "", None),
    ("dd_lon1", "", None),
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
    item = FN121(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "dd_lat",
        40.6,
        "ensure this value is greater than or equal to 41.6",
    ),
    (
        "dd_lat",
        49.5,
        "ensure this value is less than or equal to 49.1",
    ),
    (
        "dd_lat1",
        40.6,
        "ensure this value is greater than or equal to 41.6",
    ),
    (
        "dd_lat1",
        49.5,
        "ensure this value is less than or equal to 49.1",
    ),
    (
        "dd_lon",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon",
        -75.0,
        "ensure this value is less than or equal to -76.3",
    ),
    (
        "dd_lon1",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon1",
        -75.0,
        "ensure this value is less than or equal to -76.3",
    ),
    (
        "effdur",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "sidep",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "secchi",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "grdepmin",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "grdepmax",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "effdt0",
        "foobar",
        "validation error for FN121\neffdt0\n  invalid date format",
    ),
    (
        "effdt1",
        "foobar",
        "validation error for FN121\neffdt1\n  invalid date format",
    ),
    (
        "efftm0",
        "foobar",
        "validation error for FN121\nefftm0\n  invalid time format",
    ),
    (
        "efftm1",
        "foobar",
        "validation error for FN121\nefftm1\n  invalid time format",
    ),
    (
        "effdt0",
        datetime(2018, 8, 3),
        "Set or Lift Date (2018-08-03) is not consistent with prj_cd (2019)",
    ),
    (
        "effdt1",
        datetime(2020, 8, 3),
        "Set or Lift Date (2020-08-03) is not consistent with prj_cd (2019)",
    ),
    (
        "effdt0",
        datetime(2019, 10, 3),
        "Lift date (effdt1=2019-08-03) occurs before set date(effdt0=2019-10-03)",
    ),
    (
        "xslime",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "xslime",
        9,
        "value is not a valid enumeration member;",
    ),
    (
        "xslime",
        6,
        "value is not a valid enumeration member;",
    ),
    (
        "effst",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "sitem",
        -31.1,
        "ensure this value is greater than or equal to -30",
    ),
    (
        "sitem0",
        -31.1,
        "ensure this value is greater than or equal to -30",
    ),
    (
        "sitem1",
        -31.1,
        "ensure this value is greater than or equal to -30",
    ),
    (
        "sitem",
        31.1,
        "ensure this value is less than or equal to 30",
    ),
    (
        "sitem0",
        31.1,
        "ensure this value is less than or equal to 30",
    ),
    (
        "sitem1",
        31.1,
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
        FN121(**data)

    assert msg in str(excinfo.value)
