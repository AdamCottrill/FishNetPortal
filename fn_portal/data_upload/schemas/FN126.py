from enum import Enum
from typing import Optional

from pydantic import PositiveInt, PositiveFloat, confloat, validator
from .FNBase import FNBase
from .utils import string_to_float, string_to_int, empty_to_none


class FdMesEnum(str, Enum):

    Length = "L"
    Volume = "V"
    Weight = "W"


class FN126(FNBase):
    """Pydantic model for diet data."""

    fish_id: int
    slug: str
    food: int
    taxon: str
    fdcnt: Optional[confloat(ge=0)]
    fdmes: Optional[FdMesEnum]
    fdval: Optional[PositiveFloat]
    lifestage: Optional[PositiveInt]
    comment6: Optional[str]

    _string_to_float = validator("fdval", "fdcnt", allow_reuse=True, pre=True)(
        string_to_float
    )
    _string_to_int = validator("lifestage", allow_reuse=True, pre=True)(string_to_int)
    _empty_to_none = validator("fdmes", allow_reuse=True, pre=True)(empty_to_none)
