"""=============================================================
 ~/pydantic_playground/tests/test_FN011.py
 Created: 25 Aug 2021 15:23:07

 DESCRIPTION:

  A suite of unit tests to ensure that the Pydantic model for FN011
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

from fn_portal.data_upload.schemas import FN011


@pytest.fixture()
def data():
    data = {
        "lake_id": 1,
        "protocol_id": 1,
        "prj_ldr_id": 1,
        "slug": "lha_ia19_002",
        "year": "2019",
        "prj_cd": "LHA_IA19_002",
        "prj_nm": "Fake Project",
        "prj_date0": datetime(2019, 8, 3),
        "prj_date1": datetime(2019, 8, 20),
        "comment0": "This is a fake project for testing.",
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN011(**data)

    # check attributes here:
    assert item.year == int(data["year"])
    assert item.prj_cd == data["prj_cd"]
    assert item.prj_nm == data["prj_nm"]
    assert item.comment0 == data["comment0"]
    assert item.slug == data["slug"]
    assert item.slug == item.prj_cd.lower()
    assert item.prj_date0 == data["prj_date0"].date()
    assert item.prj_date1 == data["prj_date1"].date()


required_fields = [
    "lake_id",
    "protocol_id",
    "prj_ldr_id",
    "slug",
    "year",
    "prj_cd",
    "prj_nm",
    "prj_date0",
    "prj_date1",
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
        FN011(**data)

    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
    (
        "prj_date0",
        datetime(2019, 9, 20),
        "Project end date (prj_date1) occurs before start date(prj_date0).",
    ),
    (
        "prj_date1",
        datetime(2019, 7, 20),
        "Project end date (prj_date1) occurs before start date(prj_date0).",
    ),
    (
        "prj_cd",
        "foobar",
        'string does not match regex "[A-Z]{3}\\_[A-Z]{2}\\d{2}\\_[A-Z0-9]{3}',
    ),
    ("year", "2010", "Year (2010) is not consistent with prj_cd year (2019)"),
    (
        "prj_date0",
        datetime(2010, 8, 3),
        "Year of start date (prj_date0=2010-08-03) is not consistent with prj_cd (2019)",
    ),
    (
        "prj_date1",
        datetime(2020, 8, 20),
        "Year of end date (prj_date1=2020-08-20) is not consistent with prj_cd (2019)",
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
        FN011(**data)

    assert msg in str(excinfo.value)
