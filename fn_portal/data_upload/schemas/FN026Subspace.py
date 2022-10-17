from typing import Optional

from pydantic import PositiveFloat, confloat, constr, validator

from .FNBase import FNBase
from .utils import not_specified, string_to_float, to_uppercase, strip_0


class FN026Subspace(FNBase):

    slug: str
    space_id: int

    subspace: constr(regex="^([A-Z0-9]{1,6})$", max_length=6)
    subspace_des: constr(strip_whitespace=True)
    grdep_ge: Optional[confloat(ge=0)] = None
    grdep_lt: Optional[PositiveFloat] = None
    sidep_ge: Optional[confloat(ge=0)] = None
    sidep_lt: Optional[PositiveFloat] = None

    subspace_wt: Optional[confloat(gt=0, le=1)] = None

    dd_lat: Optional[confloat(ge=41.6, le=49.2)] = None
    dd_lon: Optional[confloat(ge=-89.6, le=-74.32)] = None

    class Config:
        validate_assignment = True

    _to_uppercase = validator("subspace", allow_reuse=True, pre=True)(to_uppercase)

    _to_titlecase = validator("subspace_des", allow_reuse=True, pre=True)(not_specified)

    _strip_0 = validator("dd_lat", "dd_lon", allow_reuse=True, pre=True)(strip_0)

    _string_to_float = validator(
        "grdep_ge",
        "grdep_lt",
        "sidep_ge",
        "sidep_lt",
        "subspace_wt",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

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
