from typing import Optional, Union

from pydantic import PositiveFloat, constr, confloat, validator


from .FNBase import FNBase
from .utils import string_to_float


class FN122(FNBase):
    """ """

    slug: str
    sample_id: int

    eff: constr(regex="^([A-Z0-9]{1,3})$", max_length=3)

    effdst: Optional[PositiveFloat] = None
    grdep: Optional[PositiveFloat] = None
    grtem0: Optional[confloat(ge=-30, le=30)] = None
    grtem1: Optional[confloat(ge=-30, le=30)] = None

    waterhaul: bool = False
    comment2: Optional[str]

    class Config:
        validate_assignment = True

    @validator("waterhaul", pre=True, always=True)
    def set_waterhaul(cls, waterhaul):
        return waterhaul or False

    _string_to_float = validator(
        "effdst", "grdep", "grtem0", "grtem1", allow_reuse=True, pre=True
    )(string_to_float)
