import pytest
from pydantic import ValidationError

from fn_portal.data_upload.schemas import FN124


@pytest.fixture()
def data():
    data = {
        "slug": "lha_ia19_002-1-001-091-00-50",
        "catch_id": 1,
        "siz": 50,
        "sizcnt": 4,
    }
    return data


def test_valid_data(data):
    """

    Arguments:
    - `data`:
    """

    item = FN124(**data)

    assert item.catch_id == data["catch_id"]
    assert item.slug == data["slug"]


required_fields = ["slug", "catch_id", "siz", "sizcnt"]


@pytest.mark.parametrize("fld", required_fields)
def test_required_fields(data, fld):
    """Verify that the required fields without custome error message
    raise the default messge if they are not provided.


    Arguments:
    - `data`:

    """

    data[fld] = None

    with pytest.raises(ValidationError) as excinfo:
        FN124(**data)
    msg = "none is not an allowed value"
    assert msg in str(excinfo.value)


error_list = [
    (
        "siz",
        -4,
        "ensure this value is greater than or equal to 10",
    ),
    (
        "siz",
        9,
        "ensure this value is greater than or equal to 10",
    ),
    (
        "sizcnt",
        -4,
        "ensure this value is greater than 0",
    ),
    (
        "sizcnt",
        0,
        "ensure this value is greater than 0",
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
        FN124(**data)

    assert msg in str(excinfo.value)
