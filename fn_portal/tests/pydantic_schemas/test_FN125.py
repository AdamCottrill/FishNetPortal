"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN125.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN125
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

from fn_portal.data_upload.schemas import FN125


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-1",
        "catch_id": 1,
        "fish": 2,
        "rwt": 1100,
        "flen": 440,
        "tlen": 450,
        "girth": None,
        "sex": "1",
        "mat": "2",
        "gon": "20",
        "clipc": "5",
        "clipa": None,
        "nodc": None,
        "noda": None,
        "tissue": "B",
        "agest": "14A",
        "fate": "K",
        "age_flag": True,
        "lam_flag": True,
        "stom_flag": False,
        "tag_flag": True,
        "comment5": "fn125 comment",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN125(**data)

    assert item.catch_id == data["catch_id"]
    assert item.slug == data["slug"]


required_fields = ["slug", "catch_id", "fish"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN125(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "rwt",
    "flen",
    "tlen",
    "girth",
    "sex",
    "mat",
    "gon",
    "clipc",
    "clipa",
    "nodc",
    "noda",
    "tissue",
    "agest",
    "fate",
    "age_flag",
    "lam_flag",
    "stom_flag",
    "tag_flag",
    "comment5",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN125 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN125(**data)
    assert item.slug == data["slug"]


mode_list = [
    # field, input, output
    ("tlen", "", None),
    ("flen", "", None),
    ("rwt", "", None),
    ("girth", "", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  GRP should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN125(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "flen",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "tlen",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "rwt",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "girth",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "sex",
        8,
        "value is not a valid enumeration member;",
    ),
    (
        "gon",
        88,
        "value is not a valid enumeration member;",
    ),
    (
        "mat",
        88,
        "value is not a valid enumeration member;",
    ),
    (
        "agest",
        "14Q",
        "Unknown aging structures (Q) found in AGEST (14Q)",
    ),
    (
        "clipc",
        "14Q",
        "Unknown clip code (Q) found in clipa/clipc (14Q)",
    ),
    (
        "clipa",
        "14Q",
        "Unknown clip code (Q) found in clipa/clipc (14Q)",
    ),
    # flen vs tlen
    (
        "flen",
        "500",
        "TLEN (450) must be greater than or equal to FLEN (500)",
    ),
    # condition
    (
        "rwt",
        "120",
        "FLEN/TLEN (440) is too large for the round weight (RWT=120)",
    ),
    (
        "rwt",
        "120",
        "FLEN/TLEN (450) is too large for the round weight (RWT=120)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (440) is too short for the round weight (RWT=4000)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (450) is too short for the round weight (RWT=4000)",
    ),
    # ascii-sorting:
    (
        "agest",
        "41",
        "Found non-ascii sorted value (41) found in clipa/clipc/agest or tissue (it should be: 14",
    ),
    (
        "clipa",
        "41",
        "Found non-ascii sorted value (41) found in clipa/clipc/agest or tissue (it should be: 14",
    ),
    (
        "clipc",
        "41",
        "Found non-ascii sorted value (41) found in clipa/clipc/agest or tissue (it should be: 14",
    ),
    (
        "tissue",
        "41",
        "Found non-ascii sorted value (41) found in clipa/clipc/agest or tissue (it should be: 14",
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
        FN125(**data)

    assert msg in str(excinfo.value)
