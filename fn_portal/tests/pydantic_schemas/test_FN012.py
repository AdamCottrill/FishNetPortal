"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN012.py
 Created: 25 Feb 2022 13:47:14

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN012
  objects validate as expected.

  The script includes a dictionary that representes complete, valid
  data, it then includes a list of required fields that are
  systematically omitted, and finally a list of changes to the
  dictionary of good data that invalidates it in a known way and
  verifies that pydantic raises the expected exception.

 A. Cottrill
=============================================================

"""


import pytest
from pydantic import ValidationError
from datetime import datetime

from fn_portal.data_upload.schemas import FN012


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-091-00",
        "project_id": 1,
        "species_id": 1,
        "grp": "00",
        "grp_des": "default group",
        "biosam": "1",
        "sizsam": "1",
        "sizatt": "flen",
        "sizint": 1,
        "fdsam": "0",
        "spcmrk": "0",
        "agedec": "X0",
        "flen_min": 150,
        "flen_max": 750,
        "tlen_min": 150,
        "tlen_max": 750,
        "rwt_min": 100,
        "rwt_max": 2500,
        "k_min_error": 0.2,
        "k_min_warn": 0.5,
        "k_max_error": 3.5,
        "k_max_warn": 3.0,
    }
    return data


def test_valid_base_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN012(**data)

    assert item.slug == data["slug"]
    assert item.project_id == data["project_id"]
    assert item.species_id == data["species_id"]
    assert item.grp == data["grp"]
    assert item.biosam == data["biosam"]
    assert item.sizsam == data["sizsam"]
    assert item.sizatt == data["sizatt"]
    assert item.sizint == data["sizint"]
    assert item.fdsam == data["fdsam"]
    assert item.spcmrk == data["spcmrk"]
    assert item.agedec == data["agedec"]


required_fields = [
    "slug",
    "project_id",
    "species_id",
    "grp",
    "grp_des",
    "biosam",
    "sizsam",
    "sizatt",
    "sizint",
    "fdsam",
    "spcmrk",
    "agedec",
    "flen_min",
    "flen_max",
    "tlen_min",
    "tlen_max",
    "rwt_min",
    "rwt_max",
    "k_min_error",
    "k_min_warn",
    "k_max_error",
    "k_max_warn",
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
        FN012(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
    (
        "grp",
        "AA1",
        "ensure this value has at most 2 characters",
    ),
    (
        "biosam",
        "AA1",
        "value is not a valid enumeration member",
    ),
    (
        "sizsam",
        "AA1",
        "value is not a valid enumeration member",
    ),
    (
        "sizatt",
        "AA1",
        "value is not a valid enumeration member",
    ),
    (
        "sizint",
        "AA1",
        "value is not a valid integer",
    ),
    (
        "sizint",
        "0",
        "ensure this value is greater than or equal to 1",
    ),
    (
        "sizint",
        "100",
        "ensure this value is less than or equal to 50",
    ),
    (
        "fdsam",
        "ZZ",
        "string does not match regex",
    ),
    (
        "spcmrk",
        "ZZ",
        "string does not match regex",
    ),
    (
        "agedec",
        "ZZ",
        "string does not match regex",
    ),
    (
        "flen_min",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "flen_min",
        "1000",
        "ensure this value is less than 700",
    ),
    (
        "flen_max",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "flen_max",
        "3000",
        "ensure this value is less than 2000",
    ),
    (
        "tlen_min",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "tlen_min",
        "1000",
        "ensure this value is less than 700",
    ),
    (
        "tlen_max",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "tlen_max",
        "3000",
        "ensure this value is less than 2000",
    ),
    (
        "rwt_min",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "rwt_min",
        "6000",
        "ensure this value is less than 5000",
    ),
    (
        "rwt_max",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "rwt_max",
        "6000",
        "ensure this value is less than 5000",
    ),
    (
        "k_min_error",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "k_min_error",
        "2.5",
        "ensure this value is less than 2.0",
    ),
    (
        "k_min_warn",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "k_min_warn",
        "2.5",
        "ensure this value is less than 1.5",
    ),
    (
        "k_max_error",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "k_max_error",
        "5.5",
        "ensure this value is less than 5.0",
    ),
    (
        "k_max_warn",
        "0",
        "ensure this value is greater than 0",
    ),
    (
        "k_max_warn",
        "4.5",
        "ensure this value is less than 4.0",
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
        FN012(**data)
    assert msg in str(excinfo.value)
