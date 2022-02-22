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
    ("agest", "24AMV", "24AMV"),
    ("tissue", "18D", "18D"),
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
        "string does not match regex",
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
        "tissue",
        "14Q",
        "Unknown tissue code (Q) found in TISSUE (14Q)",
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
        "FLEN/TLEN (440) is too large for the round weight (RWT=120.0)",
    ),
    (
        "rwt",
        "120",
        "FLEN/TLEN (450) is too large for the round weight (RWT=120.0)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (440) is too short for the round weight (RWT=4000.0)",
    ),
    (
        "rwt",
        "4000",
        "FLEN/TLEN (450) is too short for the round weight (RWT=4000.0)",
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


def test_rwt_between_0_and_1(data):
    """The original validator required rwt to be a constrained integer, >
    0, which meant that very small larval fish could not be captured. 0.25
    grams was converted to 0 (invalid) or 1 valid but wrong.

    This test set flen and tlen to null so that they don't tip the condition factor errors.

    Arguments:
    - `data`:

    """
    rwt = 0.25
    data["rwt"] = rwt
    data["flen"] = None
    data["tlen"] = None
    item = FN125(**data)

    assert item.rwt == rwt


valid_gon_codes = [
    "1",
    "10",
    "2",
    "20",
    "202",
    "203",
    "204",
    "205",
    "208",
    "20A",
    "20B",
    "21",
    "212",
    "213",
    "214",
    "215",
    "216",
    "217",
    "218",
    "21A",
    "21B",
    "21D",
    "21E",
    "22",
    "222",
    "223",
    "224",
    "225",
    "226",
    "227",
    "228",
    "22A",
    "22B",
    "22C",
    "22E",
    "23",
    "233",
    "235",
    "236",
    "23A",
    "23B",
    "3",
    "30",
    "305",
    "4",
    "40",
    "402",
    "403",
    "405",
    "406",
    "407",
    "40A",
    "40B",
    "40C",
    "40E",
    "9",
    "99",
    "99C",
]


@pytest.mark.parametrize("value", valid_gon_codes)
def test_valid_gonad_codes(data, value):
    """This test verified that valid gonad codes from real samples are
    recognized as valid by our gonad code regex.

    Arguments:
    - `data`:

    """

    data["gon"] = value
    item = FN125(**data)
    item_dict = item.dict()
    assert item_dict["gon"] == value


invalid_gon_codes = [
    "91",
    "100",
    "191",
    "2 0",
    "200",
    "219",
    "21X",
    "20F",
    "21F",
    "22.",
    "220",
    "221",
    "22F",
    "22X",
    "244",
    "30F",
    "40F",
    "40G",
    "99F",
    "A",
    "B",
    "C",
    "E",
    "F",
]


@pytest.mark.parametrize("code", invalid_gon_codes)
def test_invalid_gon_data(data, code):
    """This test verifies that actual invalid gonad codes from our
    database are trapped by the gonad code regular expression.

    Arguments:
    - `data`:

    """
    data["gon"] = code
    with pytest.raises(ValidationError) as excinfo:
        FN125(**data)

    msg = "string does not match regex"

    assert msg in str(excinfo.value)
