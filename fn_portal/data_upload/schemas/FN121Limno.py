from typing import Optional, Union

from pydantic import PositiveFloat, constr, confloat, validator


from .FNBase import FNBase
from .utils import string_to_float


class FN121Limno(FNBase):
    """A pydandic schema model to validate FN121Limno objects.  slug and
    sample_id are required, the other fields represent limnological (water
    chemistry) data. They can be null, but mist be constrained to
    plausible values.
    """

    slug: str
    sample_id: int

    o2gear0: Optional[confloat(ge=0, le=20)] = None
    o2gear1: Optional[confloat(ge=0, le=20)] = None
    o2bot0: Optional[confloat(ge=0, le=20)] = None
    o2bot1: Optional[confloat(ge=0, le=20)] = None
    o2surf0: Optional[confloat(ge=0, le=20)] = None
    o2surf1: Optional[confloat(ge=0, le=20)] = None

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "o2gear0",
        "o2gear1",
        "o2bot0",
        "o2bot1",
        "o2surf0",
        "o2surf1",
        allow_reuse=True,
        pre=True,
    )(string_to_float)
