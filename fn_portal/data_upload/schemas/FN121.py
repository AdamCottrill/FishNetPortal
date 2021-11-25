from datetime import date, time, datetime
from typing import Optional

from pydantic import PositiveFloat, validator, confloat

from .utils import yr_to_year, string_to_float
from .FNBase import FNBase, prj_cd_regex

from enum import IntEnum


class EffstEnum(IntEnum):
    valid = 1
    invalid = 9


class XslimeEnum(IntEnum):
    none = 0
    present = 1
    light = 2
    moderate = 3
    heavy = 4
    very_heavy = 5


class FN121(FNBase):
    """parser/validator for FN011 objects:

    + Valid project code.
    + Year must be consistent with project code
    + slug is lowercase prj_cd
    + effdt0 must be constistent with prj_cd
    + effdt1 must be constistent with prj_cd and occur on or after effdt0

    """

    grid5_id: int
    project_id: int
    ssn_id: int
    space_id: int
    mode_id: int
    slug: str

    sam: str

    effdt0: Optional[date]
    efftm0: Optional[time]
    effdt1: Optional[date]
    efftm1: Optional[time]
    effdur: Optional[PositiveFloat] = None

    effst: Optional[EffstEnum]

    # stratum: Optional[str]
    # area: Optional[str]
    sitp: Optional[str]
    site: Optional[str]

    dd_lat: Optional[confloat(ge=41.6, le=49.1)] = None
    dd_lon: Optional[confloat(ge=-89.6, le=-76.3)] = None

    dd_lat1: Optional[confloat(ge=41.6, le=49.1)] = None
    dd_lon1: Optional[confloat(ge=-89.6, le=-76.3)] = None

    sitem: Optional[confloat(ge=-30, le=30)] = None
    sitem0: Optional[confloat(ge=-30, le=30)] = None
    sitem1: Optional[confloat(ge=-30, le=30)] = None

    sidep: Optional[PositiveFloat] = None
    # grdep: Union[None, PositiveFloat, EmptyStrToNone]
    grdepmin: Optional[confloat(ge=0)] = None
    grdepmax: Optional[PositiveFloat] = None

    secchi: Optional[PositiveFloat] = None
    xslime: Optional[XslimeEnum]

    crew: Optional[str]
    comment1: Optional[str]

    _string_to_float = validator(
        "dd_lat",
        "dd_lon",
        "dd_lat1",
        "dd_lon1",
        "sidep",
        "effdur",
        "grdepmin",
        "grdepmax",
        "secchi",
        "sitem",
        "sitem0",
        "sitem1",
        allow_reuse=True,
        pre=True,
    )(string_to_float)

    @validator("dd_lat", "dd_lon", "dd_lat1", "dd_lon1", pre=True)
    def strip_0(cls, v):
        """Lat lon can be null, but they cannot be 0."""
        if v == 0:
            return None
        return v

    @validator("efftm0", "efftm1", pre=True)
    def strip_date(cls, v):
        """pyodbc treats times as datetimes. we need to strip the date off if
        it is there."""
        if isinstance(v, datetime):
            return v.time()
        return v

    @validator("effdt0", "effdt1")
    @classmethod
    def date_matches_prj_cd(cls, v, values):
        if v:
            prj_cd_yr = yr_to_year(values.get("slug", "")[6:8])
            date_yr = str(v.year)
            if prj_cd_yr != date_yr:
                err_msg = f"""Set or Lift Date ({v}) is not consistent with prj_cd ({prj_cd_yr})."""
                raise ValueError(err_msg)
        return v

    @validator("effdt1")
    def effdt0_before_effdt1(cls, v, values):
        effdt0 = values.get("effdt0")
        if v and effdt0:
            if effdt0 > v:
                raise ValueError(
                    f"Lift date (effdt1={v}) occurs before set date(effdt0={effdt0})."
                )
        return v

    @validator("grdepmax")
    def grdepmin_lte_grdepmax(cls, v, values):
        grdepmin = values.get("grdepmin")
        if v and grdepmin:
            if v < grdepmin:
                raise ValueError(
                    f"grdepmax ({v} m) must be greater than or equal to grdepmin ({grdepmin} m)."
                )
        return v
