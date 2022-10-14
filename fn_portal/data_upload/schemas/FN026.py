from typing import Optional

from pydantic import confloat, PositiveFloat, validator, constr

from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase, strip_0


class FN026(FNBase):

    slug: str
    project_id: int

    space: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    space_des: constr(strip_whitespace=True)
    grdep_ge: Optional[confloat(ge=0)] = None
    grdep_lt: Optional[PositiveFloat] = None
    sidep_ge: Optional[confloat(ge=0)] = None
    sidep_lt: Optional[PositiveFloat] = None
    space_wt: Optional[confloat(gt=0, le=1)] = None

    dd_lat: Optional[confloat(ge=41.6, le=49.1)] = None
    dd_lon: Optional[confloat(ge=-89.6, le=-74.32)] = None

    class Config:
        validate_assignment = True

    _to_uppercase = validator("space", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("space_des", allow_reuse=True, pre=True)(not_specified)

    _string_to_float = validator(
        "grdep_ge",
        "grdep_lt",
        "sidep_ge",
        "sidep_lt",
        "space_wt",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    _strip_0 = validator("dd_lat", "dd_lon", allow_reuse=True, pre=True)(strip_0)

    @validator("dd_lon")
    def dd_lat_and_dd_lon(cls, v, values):
        dd_lat = values.get("dd_lat")
        if v and dd_lat:
            return v
        if v and dd_lat is None:
            raise ValueError(
                "dd_lat must be populated with a valid latitude if dd_lon is provided."
            )
        if v is None and dd_lat:
            raise ValueError(
                "dd_lon must be populated with a valid longitude if dd_lat is provided."
            )
        return v
