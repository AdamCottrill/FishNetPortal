"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/pydantic_playground/tests/test_FN022.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN022
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

from fn_portal.data_upload.schemas import FN022


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-01",
        "project_id": 1,
        "ssn": "01",
        "ssn_des": "the summer",
        "ssn_date0": datetime(2019, 8, 3),
        "ssn_date1": datetime(2019, 8, 20),
    }
    return data


def test_valid_base_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN022(**data)

    assert item.project_id == data["project_id"]
    assert item.slug == data["slug"]
    assert item.ssn_des == data["ssn_des"].title()
    assert item.ssn_date0 == data["ssn_date0"].date()
    assert item.ssn_date1 == data["ssn_date1"].date()


required_fields = [
    "slug",
    "project_id",
    "ssn",
    "ssn_date0",
    "ssn_date1",
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
        FN022(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


ssn_list = [("aa", "AA"), ("a1", "A1"), ("AA", "AA"), ("A1", "A1"), ("00", "00")]


@pytest.mark.parametrize("ssn_in,ssn_out", ssn_list)
def test_valid_ssn(data, ssn_in, ssn_out):
    """Season should be a two letter code made from uppercase letters or
    digits.  The pydantic model should convert any letters to
    uppercase automatically. Uppercase letters and any numbers should
    be returned unchanged.

    Arguments:
    - `data`:

    """
    data["ssn"] = ssn_in
    item = FN022(**data)

    assert item.ssn == ssn_out


error_list = [
    (
        "ssn",
        "AA1",
        "ensure this value has at most 2 characters",
    ),
    (
        "ssn",
        "A*",
        'string does not match regex "^([A-Z0-9]{2})$"',
    ),
    (
        "ssn_date0",
        datetime(2019, 9, 20),
        "Season end date (ssn_date1=2019-08-20) occurs before start date(ssn_date0=2019-09-20)",
    ),
    (
        "ssn_date0",
        datetime(2018, 8, 3),
        "Year of start date (ssn_date0=2018-08-03) is not consistent with prj_cd (2019)",
    ),
    (
        "ssn_date1",
        datetime(2020, 8, 20),
        "Year of end date (ssn_date1=2020-08-20) is not consistent with prj_cd (2019)",
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
        FN022(**data)

    assert msg in str(excinfo.value)
