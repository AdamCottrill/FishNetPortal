"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN127.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN127
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

from fn_portal.data_upload.schemas import FN127Factory


@pytest.fixture()
def choices():

    agest_choices = "01234567ABCDEFGMKT"
    ageprep1_choices = "0123456789CKT"
    ageprep2_choices = "12349"

    return {
        "agest_choices": agest_choices,
        "ageprep1_choices": ageprep1_choices,
        "ageprep2_choices": ageprep2_choices,
    }


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00",
        "fish_id": 1,
        "ageid": 1,
        "preferred": True,
        "agea": 8,
        "agemt": "A2345",
        "edge": "++",
        "conf": 7,
        "nca": 7,
        "comment7": "test record",
    }
    return data


def test_valid_data(data, choices):
    """

    Arguments:
    - `data`:
    """

    FN127 = FN127Factory(**choices)
    item = FN127(**data)

    assert item.fish_id == data["fish_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "fish_id",
    "ageid",
    "agemt",
    "preferred",
]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, choices, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    FN127 = FN127Factory(**choices)

    with pytest.raises(ValidationError) as excinfo:
        FN127(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = ["agea", "edge", "conf", "nca", "comment7"]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, choices, fld):
    """Verify that the FN127 item is created without error if an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    FN127 = FN127Factory(**choices)
    item = FN127(**data)
    assert item.slug == data["slug"]


mode_list = [
    # field, input, output
    ("agea", "", None),
    ("agea", "0", 0),
    ("agea", 0, 0),
    ("nca", "", None),
    ("nca", "0", 0),
    ("nca", 0, 0),
    ("conf", "", None),
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
    FN127 = FN127Factory(**choices)
    item = FN127(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "agea",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "nca",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    (
        "edge",
        "foo",
        "value is not a valid enumeration member;",
    ),
    (
        "agemt",
        "foobar",
        "ensure this value has at most 5 characters",
    ),
    (
        "agemt",
        "A",
        'string does not match regex "^([A-Z0-9]{5})$"',
    ),
    (
        "agemt",
        "A124*",
        'string does not match regex "^([A-Z0-9]{5})$"',
    ),
    ("agemt", "Z1111", "Unknown aging structure (Z) found in agemt (Z1111)"),
    ("agemt", "1Z111", "Unknown aging prep1 method (Z) found in agemt (1Z111)"),
    ("agemt", "11Z11", "Unknown aging prep2 method (Z) found in agemt (11Z11)"),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, choices, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    FN127 = FN127Factory(**choices)

    with pytest.raises(ValidationError) as excinfo:
        FN127(**data)

    assert msg in str(excinfo.value)
