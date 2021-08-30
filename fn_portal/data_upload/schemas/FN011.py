from datetime import date
from typing import Optional

from pydantic import validator, constr

from .utils import to_titlecase, yr_to_year

from .FNBase import FNBase, prj_cd_regex


class FN011(FNBase):
    """parser/validator for FN011 objects:

    + Valid project code.
    + Year must be consistent with project code
    + slug is lowercase prj_cd
    + prj_date0 must be constistent with prj_cd
    + prj_date1 must be constistent with prj_cd and occur on or after prj_date0

    """

    lake_id: int
    protocol_id: int
    prj_ldr_id: int
    slug: str
    prj_cd: constr(regex=prj_cd_regex)
    year: int
    prj_nm: str
    prj_date0: date
    prj_date1: date

    comment0: Optional[str]

    _prj_nm_titlecase = validator("prj_nm", allow_reuse=True)(to_titlecase)

    @validator("year")
    def check_year_with_prj_cd(cls, v, values):

        prj_cd_yr = yr_to_year(values.get("prj_cd", "")[6:8])
        if int(prj_cd_yr) != v:
            prj_cd = values.get("prj_cd")
            err_msg = f"""{prj_cd}: Year ({v}) is not consistent with prj_cd year ({prj_cd_yr})."""
            raise ValueError(err_msg)
        return v

    @validator("prj_date0")
    @classmethod
    def prj_date0_matches_prj_cd(cls, v, values):

        prj_cd_yr = yr_to_year(values.get("prj_cd", "")[6:8])
        date_yr = str(v.year)
        if prj_cd_yr != date_yr:
            prj_cd = values.get("prj_cd")
            err_msg = f"""{prj_cd}: Year of start date (prj_date0={v}) is not consistent with prj_cd ({prj_cd_yr})."""
            raise ValueError(err_msg)
        return v

    @validator("prj_date1")
    def prj_date0_before_prj_date1(cls, v, values):

        if values.get("prj_date0") > v:
            raise ValueError(
                "Project end date (prj_date1) occurs before start date(prj_date0)."
            )
        return v

    @validator("prj_date1")
    @classmethod
    def prj_date1_matches_prj_cd(cls, v, values):
        prj_cd_yr = yr_to_year(values.get("prj_cd", "")[6:8])
        date_yr = str(v.year)
        if prj_cd_yr != date_yr:
            prj_cd = values.get("prj_cd")
            err_msg = f"""{prj_cd}: Year of end date (prj_date1={v}) is not consistent with prj_cd ({prj_cd_yr})."""
            raise ValueError(err_msg)
        return v
