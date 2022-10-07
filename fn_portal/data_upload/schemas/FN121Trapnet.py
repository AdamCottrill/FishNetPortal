from enum import IntEnum
from typing import Optional

from pydantic import confloat, validator

from .FNBase import FNBase
from .utils import string_to_float, string_to_int


class VegetationEnum(IntEnum):

    none = 1
    sparse = 2
    moderate = 3
    dense = 4


class FN121Trapnet(FNBase):
    """A pydandic schema model to validate FN121Trawl objects.  slug
    and sample_id are required, the other fields represent trawl
    attribute data. They can be null, but mist be constrained to
    plausible values.

    """

    slug: str
    sample_id: int

    cover_id: Optional[int] = None
    bottom_id: Optional[int] = None

    vegetation: Optional[VegetationEnum] = None
    lead_angle: Optional[confloat(ge=0, le=90)] = None
    leaduse: Optional[confloat(ge=0)] = None
    distoff: Optional[confloat(ge=0)] = None

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "lead_angle",
        "leaduse",
        "distoff",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    _string_to_int = validator("vegetation", allow_reuse=True, pre=True)(string_to_int)
