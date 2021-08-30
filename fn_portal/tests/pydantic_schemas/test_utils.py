import pytest
from fn_portal.data_upload.schemas.utils import (
    string_to_int,
    string_to_float,
    empty_to_none,
    to_titlecase,
    to_uppercase,
    not_specified,
    yr_to_year,
)


to_float = [
    ("10", 10.0),
    ("3.14", 3.14),
    ("", None),
    (None, None),
]


@pytest.mark.parametrize("value_in,value_out", to_float)
def test_string_to_float(value_in, value_out):
    """ """
    assert string_to_float(value_in) == value_out


to_int = [
    ("10", 10),
    ("", None),
    (None, None),
]


@pytest.mark.parametrize("value_in,value_out", to_int)
def test_string_to_int(value_in, value_out):
    """ """
    assert string_to_int(value_in) == value_out


to_none = [
    ("10", "10"),
    (3.14, 3.14),
    ("Unchanged", "Unchanged"),
    ("", None),
    (None, None),
]


@pytest.mark.parametrize("value_in,value_out", to_none)
def test_empty_to_none(value_in, value_out):
    """ """
    assert empty_to_none(value_in) == value_out


titlecase_list = [
    ("this will change", "This Will Change"),
    ("THIS WILL CHANGE", "This Will Change"),
    ("Unchanged", "Unchanged"),
    ("", ""),
    (None, None),
]


@pytest.mark.parametrize("value_in,value_out", titlecase_list)
def test_to_titlecase(value_in, value_out):
    """ """
    assert to_titlecase(value_in) == value_out


uppercase_list = [
    ("this will change", "THIS WILL CHANGE"),
    ("This Will Change", "THIS WILL CHANGE"),
    ("UNCHANGED", "UNCHANGED"),
    ("", ""),
    (None, None),
]


@pytest.mark.parametrize("value_in,value_out", uppercase_list)
def test_to_uppercase(value_in, value_out):
    """ """
    assert to_uppercase(value_in) == value_out


not_specified_list = [
    ("this will change", "This Will Change"),
    ("THIS WILL CHANGE", "This Will Change"),
    ("Unchanged", "Unchanged"),
    ("", "Not Specified"),
    (None, "Not Specified"),
]


@pytest.mark.parametrize("value_in,value_out", not_specified_list)
def test_not_specified(value_in, value_out):
    """ """
    assert not_specified(value_in) == value_out


yr_list = [
    ("50", "1950"),
    ("99", "1999"),
    ("00", "2000"),
    ("20", "2020"),
]


@pytest.mark.parametrize("value_in,value_out", yr_list)
def test_yr_to_year(value_in, value_out):
    """ """
    assert yr_to_year(value_in) == value_out
