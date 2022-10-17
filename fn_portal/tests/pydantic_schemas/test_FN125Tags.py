"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN125Tags.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN125Tags
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

from fn_portal.data_upload.schemas import FN125Tags


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-1-2",
        "fish_id": 1,
        "fish_tag_id": 1,
        "tagid": "123654A",
        "tagdoc": "25012",
        "tagstat": "C",
        "cwtseq": None,
        "comment_tag": "not a real tag",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN125Tags(**data)

    assert item.fish_id == data["fish_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "fish_id",
    "fish_tag_id",
    "tagdoc",
    "tagstat",
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
        FN125Tags(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = ["cwtseq", "comment_tag"]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN125Tags item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN125Tags(**data)
    assert item.slug == data["slug"]


mode_list = [
    # field, input, output
    ("cwtseq", "", None),
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
    item = FN125Tags(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "cwtseq",
        -4,
        "ensure this value is greater than 0",
    ),
    ("tagstat", "X", "value is not a valid enumeration member;"),
    ("tagdoc", "X", "ensure this value has at least 5 characters"),
    ("tagdoc", "1234567", "ensure this value has at most 5 characters"),
    ("tagdoc", "1234*", 'string does not match regex "^([A-Z0-9]{5})$"'),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN125Tags(**data)

    assert msg in str(excinfo.value)


# THere are some co-dependencies between fields - some combination are
# valid, other are not.  These tests check first to ensure that valid
# combination work, and then that invalid ones are caught and reported
# appropriately:

valid_combinations = [
    # tag stat can be N if tag is is empy and tagdoc starts with 6 or p
    {"tagstat": "N", "tagid": None, "tagdoc": "P1234"},
    {"tagstat": "N", "tagid": None, "tagdoc": "61234"},
]


@pytest.mark.parametrize("fld_values", valid_combinations)
def test_valid_field_combinations(data, fld_values):
    """

    Arguments:
    - `data`:
    """

    data.update(fld_values)
    item = FN125Tags(**data)

    assert item.fish_id == data["fish_id"]
    assert item.slug == data["slug"]


invalid_combinations = [
    # tag stat can be N if tag is is empy and tagdoc starts with 6 or p
    [
        {"tagstat": "N", "tagid": 1234, "tagdoc": "P1234"},
        "TAGSTAT cannot be 'N' if TAGID is populated (TAGID='1234')",
    ],
    [
        {"tagstat": "N", "tagid": 1234, "tagdoc": "21234"},
        "TAGSTAT='N' is only allowed if TAGTYPE is 6 (CWT) or P (PIT).",
    ],
    [
        {"tagstat": "A", "tagid": None, "tagdoc": "21234"},
        "TAGID cannot be empty if TAGSTAT='A' (tag applied).",
    ],
]


@pytest.mark.parametrize("fld_values,msg", invalid_combinations)
def test_invalid_combinations(data, fld_values, msg):
    """

    Arguments:
    - `data`:
    """
    data.update(fld_values)

    with pytest.raises(ValidationError) as excinfo:
        FN125Tags(**data)

    assert msg in str(excinfo.value)
