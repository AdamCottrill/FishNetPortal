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
        "subspace_id": 1,
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
        "dd_lat0": 45.5,
        "dd_lon0": -81.2,
        "dd_lat1": 45.6,
        "dd_lon1": -81.1,
        "sitem0": 18.1,
        "sitem1": 21.2,
        "sidep0": 10.2,
        "grdepmin": 8.2,
        "grdepmax": 11.6,
        "secchi0": 1.9,
        "secchi1": 3.5,
        "slime": None,
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
    "subspace_id",
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
    "sitem0",
    "sitem1",
    "sidep0",
    "grdepmin",
    "grdepmax",
    "secchi0",
    "secchi1",
    "slime",
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


valid_fields = [
    # gear depth can be 0, or some small number 0.1
    ("grdepmin", 0),
    ("grdepmin", 0.1),
]


@pytest.mark.parametrize("fld,value", valid_fields)
def test_valid_data(data, fld, value):
    """THis test verifies that alternive values can be provide that will
    still be valid.  This test will be used to capture values taht have
    been submitted in real datasets.

    Arguments:
    - `data`:

    """
    data[fld] = value
    item = FN121(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value


field_list = [
    # field, input, output
    ("effdur", "", None),
    ("sidep0", "", None),
    ("secchi0", "", None),
    ("secchi1", "", None),
    ("grdepmin", "", None),
    ("grdepmax", "", None),
    ("sitem0", "", None),
    ("sitem1", "", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", field_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some
    optional fields.  For example fields that contain an empty string
    should be converted to None to eliminate empty strings in our
    master dataset.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN121(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


paired_field_list = [
    ("dd_lat0", "dd_lon0", "", None),
    ("dd_lat1", "dd_lon1", "", None),
    ("dd_lat0", "dd_lon0", "0", None),
    ("dd_lat1", "dd_lon1", "0", None),
]


@pytest.mark.parametrize("fld1,fld2,value_in,value_out", paired_field_list)
def test_paired_alternatives(data, fld1, fld2, value_in, value_out):
    """When the pydanic model is created, it should transform some
    optional fields.  Some fields must be transformed in pairs - lat
    and long are only valid if they are both populated, or both null.
    Arguments: - `data`:

    """
    data[fld1] = value_in
    data[fld2] = value_in
    item = FN121(**data)
    item_dict = item.dict()
    assert item_dict[fld1] == value_out
    assert item_dict[fld2] == value_out


error_list = [
    (
        "dd_lat0",
        None,
        "dd_lat0 must be populated with a valid latitude if dd_lon0 is provided",
    ),
    (
        "dd_lon0",
        None,
        "dd_lon0 must be populated with a valid longitude if dd_lat0 is provided",
    ),
    (
        "dd_lat1",
        None,
        "dd_lat1 must be populated with a valid latitude if dd_lon1 is provided",
    ),
    (
        "dd_lon1",
        None,
        "dd_lon1 must be populated with a valid longitude if dd_lat1 is provided",
    ),
    (
        "dd_lat0",
        "0",
        "dd_lat0 must be populated with a valid latitude if dd_lon0 is provided",
    ),
    (
        "dd_lon0",
        "0",
        "dd_lon0 must be populated with a valid longitude if dd_lat0 is provided",
    ),
    (
        "dd_lat1",
        "0",
        "dd_lat1 must be populated with a valid latitude if dd_lon1 is provided",
    ),
    (
        "dd_lon1",
        "0",
        "dd_lon1 must be populated with a valid longitude if dd_lat1 is provided",
    ),
    (
        "dd_lat0",
        40.6,
        "ensure this value is greater than or equal to 41.6",
    ),
    (
        "dd_lat0",
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
        "dd_lon0",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon0",
        -72.0,
        "ensure this value is less than or equal to -74.32",
    ),
    (
        "dd_lon1",
        -90.1,
        "ensure this value is greater than or equal to -89.6",
    ),
    (
        "dd_lon1",
        -72.0,
        "ensure this value is less than or equal to -74.32",
    ),
    (
        "effdur",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "sidep0",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "secchi0",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "secchi1",
        -1.0,
        "ensure this value is greater than 0",
    ),
    (
        "grdepmin",
        -1.0,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "grdepmax",
        1.0,
        "grdepmax (1.0 m) must be greater than or equal to grdepmin (8.2 m).",
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
        "slime",
        99,
        "value is not a valid enumeration member;",
    ),
    (
        "slime",
        9,
        "value is not a valid enumeration member;",
    ),
    (
        "slime",
        6,
        "value is not a valid enumeration member;",
    ),
    (
        "effst",
        99,
        "value is not a valid enumeration member;",
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
