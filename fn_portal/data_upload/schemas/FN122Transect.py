from datetime import datetime
from typing import Optional

from pydantic import confloat, validator

from .FNBase import FNBase
from .utils import string_to_float, string_to_int


class FN122Transect(FNBase):
    """A pydandic schema model to validate FN122Transect objects.
    slug and sample_id are required, the other fields represent
    transect points. They can be null, but must be
    constrained to plausible values.

    """

    slug: str
    sample_id: int
    track_id: int

    dd_lat: confloat(ge=41.7, le=49.2)
    dd_lon: confloat(ge=-89.6, le=-76.4)
    sidep: Optional[confloat(ge=0, le=400)] = None
    timestamp: Optional[datetime] = None
    comment: Optional[str] = None

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "dd_lat",
        "dd_lon",
        "sidep",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    _string_to_int = validator("track_id", allow_reuse=True, pre=True)(string_to_int)
