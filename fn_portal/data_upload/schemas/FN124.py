from pydantic import validator, conint, PositiveInt
from typing import Optional

from .FNBase import FNBase
from .utils import string_to_int


class FN124(FNBase):
    """Pydanic model for length tallies."""

    slug: str
    catch_id: PositiveInt
    siz: conint(ge=20)
    sizcnt: PositiveInt

    class Config:
        validate_assignment = True

    _string_to_int = validator("siz", "sizcnt", allow_reuse=True, pre=True)(
        string_to_int
    )
