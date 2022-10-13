"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN123NonFish.py
 Created: 26 Aug 2021 16:43:50

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN123NonFish
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

from fn_portal.data_upload.schemas import FN123NonFish


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-123456",
        "effort_id": 1,
        "taxon_id": 1,
        "catcnt": 12,
        "mortcnt": 5,
        "comment": "never seen so many.",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN123NonFish(**data)

    assert item.effort_id == data["effort_id"]
    assert item.slug == data["slug"]


required_fields = [
    "slug",
    "effort_id",
    "taxon_id",
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
        FN123NonFish(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


optional_fields = [
    "catcnt",
    "mortcnt",
    "comment",
]


@pytest.mark.parametrize("fld", optional_fields)
def test_optional_fields(data, fld):
    """Verify that the FN123NonFish item is created without error if
    an optional field is omitted

    Arguments:
    - `data`:

    """
    data[fld] = None
    item = FN123NonFish(**data)
    assert item.slug == data["slug"]


alternate_value_list = [
    # field, input, output
    ("catcnt", "", None),
    ("catcnt", "10", 10),
    ("mortcnt", "", None),
    ("mortcnt", "4", 4),
]


@pytest.mark.parametrize("fld,value_in,value_out", alternate_value_list)
def test_valid_alternatives(data, fld, value_in, value_out):
    """When the pydanic model is created, it should transform some of the
    fields, but the model should still validate.

    Arguments:
    - `data`:

    """
    data[fld] = value_in
    item = FN123NonFish(**data)
    item_dict = item.dict()
    assert item_dict[fld] == value_out


error_list = [
    (
        "catcnt",
        -4,
        "ensure this value is greater than or equal to 1",
    ),
    (
        "catcnt",
        -0,
        "ensure this value is greater than or equal to 1",
    ),
    (
        "mortcnt",
        -4,
        "ensure this value is greater than or equal to 0",
    ),
    ("mortcnt", 25, "MORTCNT (25) cannot be greater than CATCNT (12)"),
]


@pytest.mark.parametrize("fld,value,msg", error_list)
def test_invalid_data(data, fld, value, msg):
    """

    Arguments:
    - `data`:
    """

    data[fld] = value
    with pytest.raises(ValidationError) as excinfo:
        FN123NonFish(**data)

    assert msg in str(excinfo.value)
