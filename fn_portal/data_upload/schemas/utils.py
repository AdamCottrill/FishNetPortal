"""
=============================================================
~/pydantic_playground/schemas/utils.py
Created: Jul-17-2021 17:44
DESCRIPTION:

    pydantic models used to parse and validate incoming records.

A. Cottrill
=============================================================
"""

from datetime import datetime
from typing import Optional

from pydantic.validators import str_validator


def string_to_float(v) -> Optional[float]:
    """A validator that will convert floats passed in as strings to a
    python float."""

    if v is None:
        return v
    else:
        try:
            val = float(v)
        except ValueError:
            val = None
    return val


def string_to_int(v) -> Optional[int]:
    """A validator that will convert floats passed in as strings to a
    python integer"""

    if v is None:
        return v
    else:
        try:
            val = int(v)
        except ValueError:
            val = None
    return val


def empty_to_none(v: str) -> Optional[str]:
    if v == "":
        return None
    return v


def check_ascii_sort(value: str) -> Optional[str]:
    if value is not None:
        val = list(value)
        val.sort()
        val = "".join(val)
        if val != value:
            msg = f"Found non-ascii sorted value '{value}' (it should be: {val})"
            raise ValueError(msg)
    return value


def check_agest(value: str) -> Optional[str]:
    if value is not None:
        allowed = "01234567ABCDEFMTV"
        unknown = [c for c in value if c not in allowed]
        if unknown:
            msg = f"Unknown aging structures ({','.join(unknown)}) found in AGEST ({value})"
            raise ValueError(msg)
        return value


def strip_date(value):
    """pyodbc treats times as datetimes. we need to strip the date off if
    it is there."""

    if value == "":
        return None
    if isinstance(value, datetime):
        return value.time()
    return value


class EmptyStrToNone(str):
    @classmethod
    def __get_validators__(cls):
        yield str_validator
        yield empty_to_none


def to_titlecase(value: str) -> str:
    if value:
        return value.title()
    else:
        return value


def to_uppercase(value: str) -> str:
    if value:
        return value.upper()
    else:
        return value


def not_specified(value: str) -> str:
    if value:
        return value.title()
    else:
        return "Not Specified"


def yr_to_year(yr):
    if int(yr) < 50:
        return f"20{yr}"
    else:
        return f"19{yr}"


def strip_0(val):
    """Lat lon can be null, but they cannot be 0."""
    if val == 0 or val == "0" or val == "":
        return None
    return val
