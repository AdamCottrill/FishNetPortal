from enum import IntEnum
from typing import Optional

from pydantic import confloat, validator

from .FNBase import FNBase
from .utils import string_to_float, string_to_int


class VesselDirectionEnum(IntEnum):

    variable = 0
    northeast = 1
    east = 2
    southeast = 3
    south = 4
    southwest = 5
    west = 6
    northwest = 7
    north = 8
    not_definable = 9


class FN121Trawl(FNBase):
    """A pydandic schema model to validate FN121Trawl objects.  slug
    and sample_id are required, the other fields represent trawl
    attribute data. They can be null, but mist be constrained to
    plausible values.

    """

    slug: str
    sample_id: int

    vessel_id: Optional[int] = None
    vessel_speed: Optional[confloat(ge=0, le=10)] = None
    vessel_direction: Optional[VesselDirectionEnum] = None
    warp: Optional[confloat(gt=0)] = None

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "vessel_speed",
        "warp",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    _string_to_int = validator("vessel_direction", allow_reuse=True, pre=True)(
        string_to_int
    )
