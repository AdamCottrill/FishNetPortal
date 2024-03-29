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

from fn_portal.data_upload.schemas import FN125Factory


@pytest.fixture()
def choices():

    tissue_choices = "123456789ABCDEHKNV"
    clip_choices = "01234567ABCDEFG"

    return {"tissue_choices": tissue_choices, "clip_choices": clip_choices}


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-1",
        "catch_id": 1,
        "fish": "2",
        "rwt": 1100,
        "eviswt": 900,
        "flen": 440,
        "tlen": 450,
        "girth": None,
        "sex": "1",
        "mat": "2",
        "gon": "20",
        "gonwt": 10.2,
        "clipc": "5",
        "clipa": None,
        "nodc": None,
        "noda": None,
        "tissue": "B",
        "agest": "14A",
        "fate": "K",
        "stom_flag": "0",
        "stom_contents_wt": 5.5,
        "comment5": "fn125 comment",
    }
    return data


def test_valid_data(data, choices):
    """

    Arguments:
    - `data`:
    """

    FN125 = FN125Factory(**choices)
    item = FN125(**data)

    assert item.catch_id == data["catch_id"]
    assert item.slug == data["slug"]


required_fields = ["slug", "catch_id", "fish"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, choices, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None
    FN125 = FN125Factory(**choices)
    with pytest.raises(ValidationError) as excinfo:
        FN125(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "rwt",
    "eviswt",
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
    "stom_contents_wt",
    "stom_flag",
    "comment5",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, choices, fld):
    """Verify that the FN125 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    FN125 = FN125Factory(**choices)
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
    ("agest", "24amv", "24AMV"),
    ("tissue", "18d", "18D"),
    ("fish", 10, "10"),
    ("fish", "10l", "10L"),
    ("rwt", "1100.1", 1100.1),
    ("eviswt", "900.1", 900.1),
    ("gonwt", "10.1", 10.1),
    ("stom_contents_wt", "10.1", 10.1),
    ("eviswt", "", None),
    ("gonwt", "", None),
    ("stom_contents_wt", "", None),
]


@pytest.mark.parametrize("fld,value_in,value_out", mode_list)
def test_valid_alternatives(data, choices, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some fo the
    fields.  GRP should be a two letter code made from uppercase
    letters or digits.  The pydantic model should convert any letters
    to uppercase automatically. Uppercase letters and any numbers
    should be returned unchanged.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    FN125 = FN125Factory(**choices)
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
        "fish",
        "123_",
        "string does not match regex",
    ),
    (
        "fish",
        "12345AB",
        "ensure this value has at most 6 characters",
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
        "80",
        "FLEN/TLEN (440) is too large for the round weight (RWT=80.0)",
    ),
    (
        "rwt",
        "80",
        "FLEN/TLEN (450) is too large for the round weight (RWT=80.0)",
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
    ("eviswt", "1400", "EVISWT (1400.0) must be less than RWT (1100.0)"),
    # ascii-sorting:
    (
        "agest",
        "41",
        "Found non-ascii sorted value '41' (it should be: 14)",
    ),
    (
        "clipa",
        "41",
        "Found non-ascii sorted value '41' (it should be: 14)",
    ),
    (
        "clipc",
        "41",
        "Found non-ascii sorted value '41' (it should be: 14)",
    ),
    (
        "tissue",
        "41",
        "Found non-ascii sorted value '41' (it should be: 14)",
    ),
    (
        "stom_flag",
        "X",
        "value is not a valid enumeration member;",
    ),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, choices, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    FN125 = FN125Factory(**choices)
    with pytest.raises(ValidationError) as excinfo:
        FN125(**data)

    assert msg in str(excinfo.value)


def test_rwt_between_0_and_1(data, choices):
    """The original validator required rwt to be a constrained integer, >
    0, which meant that very small larval fish could not be captured. 0.25
    grams was converted to 0 (invalid) or 1 valid but wrong.

    This test set flen and tlen to null so that they don't tip the condition factor errors.

    Arguments:
    - `data`:

    """
    rwt = 0.25
    data["rwt"] = rwt
    data["eviswt"] = None
    data["flen"] = None
    data["tlen"] = None
    FN125 = FN125Factory(**choices)
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
def test_valid_gonad_codes(data, choices, value):
    """This test verified that valid gonad codes from real samples are
    recognized as valid by our gonad code regex.

    Arguments:
    - `data`:

    """

    data["gon"] = value
    FN125 = FN125Factory(**choices)
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
def test_invalid_gon_data(data, choices, code):
    """This test verifies that actual invalid gonad codes from our
    database are trapped by the gonad code regular expression.

    Arguments:
    - `data`:

    """
    data["gon"] = code
    FN125 = FN125Factory(**choices)
    with pytest.raises(ValidationError) as excinfo:
        FN125(**data)

    msg = "string does not match regex"

    assert msg in str(excinfo.value)
