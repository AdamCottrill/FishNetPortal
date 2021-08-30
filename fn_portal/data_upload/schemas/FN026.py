from typing import Optional, Union

from pydantic import confloat, PositiveFloat, validator, constr

from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase


class FN026(FNBase):

    slug: str
    project_id: int

    space: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    space_des: constr(strip_whitespace=True)
    area_lst: Optional[str] = "Not Specified"
    site_lst: Optional[str]
    sitp_lst: Optional[str]
    grdep_ge: Optional[confloat(ge=0)] = None
    grdep_lt: Optional[PositiveFloat] = None
    sidep_ge: Optional[confloat(ge=0)] = None
    sidep_lt: Optional[PositiveFloat] = None
    grid_ge: Optional[str]
    grid_lt: Optional[str]

    class Config:
        validate_assignment = True

    _to_uppercase = validator("space", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("space_des", "area_lst", allow_reuse=True, pre=True)(
        not_specified
    )

    _string_to_float = validator(
        "grdep_ge", "grdep_lt", "sidep_ge", "sidep_lt", allow_reuse=True, pre=True
    )(string_to_float)
