from datetime import datetime, time
from enum import IntEnum, Enum
from typing import Optional

from pydantic import PositiveFloat, validator, constr


from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase

# gruse and orient need to be enums
# test time constraints - valid times.


class OrientEnum(str, Enum):

    perpendicular = "1"
    paralell = "2"
    upstream = "U"
    downstream = "D"
    unknown = "9"


class GrUseEnum(IntEnum):

    bottom_set = 1
    canned = 2
    kyted = 3
    thermocline = 4
    midwater = 5
    surface = 6
    unknown = 9


class FN028(FNBase):

    gear_id: int
    project_id: int

    slug: str
    mode_des: Optional[str] = "Not Specified"
    mode: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    gruse: GrUseEnum
    orient: OrientEnum
    effdur_ge: Optional[PositiveFloat] = None
    effdur_lt: Optional[PositiveFloat] = None

    efftm0_lt: Optional[time] = None
    efftm0_ge: Optional[time] = None

    class Config:
        validate_assignment = True

    _to_uppercase = validator("mode", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("mode_des", allow_reuse=True, pre=True)(not_specified)

    _string_to_float = validator("effdur_ge", "effdur_lt", allow_reuse=True, pre=True)(
        string_to_float
    )

    @validator("efftm0_ge", "efftm0_lt", pre=True)
    def strip_date(cls, v):
        """pyodbc treats times as datetimes. we need to strip the date off if
        it is there."""
        if isinstance(v, datetime):
            return v.time()
        return v

    @validator("efftm0_ge")
    @classmethod
    def efftm0_ge_greater_than_efftm0_lt(cls, v, values, **kwargs):
        tm0_lt = values.get("efftm0_lt")
        if v and tm0_lt:
            if v > tm0_lt:
                err_msg = f"Latest set time (efftm0_lt={tm0_lt}) is earlier than earliest set time(efftm0_ge={v})"
                raise ValueError(err_msg)

        return v
