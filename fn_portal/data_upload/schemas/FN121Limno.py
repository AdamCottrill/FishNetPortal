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

    do_gear: Optional[confloat(ge=0, le=20)] = None
    xo2: Optional[confloat(ge=0, le=20)] = None
    xo22: Optional[confloat(ge=0, le=20)] = None
    surfdo2: Optional[confloat(ge=0, le=20)] = None
    surfdo22: Optional[confloat(ge=0, le=20)] = None

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "do_gear", "xo2", "xo22", "surfdo2", "surfdo22", allow_reuse=True, pre=True
    )(string_to_float)
