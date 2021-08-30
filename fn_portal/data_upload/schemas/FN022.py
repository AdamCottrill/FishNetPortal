from datetime import date

from pydantic import validator, constr

from .utils import not_specified, to_uppercase, yr_to_year
from .FNBase import FNBase


class FN022(FNBase):
    """Scrub our seasons.  Make sure that the dates are consistent with the
    project code, ssn_date0 occurs on or before ssn_date1

        TODO: ensure that seasons do not overlap within projects.
    """

    slug: str
    project_id: int
    ssn: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    ssn_des: str
    ssn_date0: date
    ssn_date1: date

    class Config:
        validate_assignment = True

    _to_uppercase = validator("ssn", allow_reuse=True, pre=True)(to_uppercase)
    _not_specified = validator("ssn_des", allow_reuse=True, pre=True)(not_specified)

    @validator("ssn_date0")
    @classmethod
    def ssn_date0_matches_prj_cd(cls, v, values):

        prj_cd_yr = yr_to_year(values.get("slug", "")[6:8])
        date_yr = str(v.year)
        if prj_cd_yr != date_yr:
            err_msg = f"""Year of start date (ssn_date0={v}) is not consistent with prj_cd ({prj_cd_yr})."""
            raise ValueError(err_msg)
        return v

    @validator("ssn_date1")
    @classmethod
    def ssn_date1_matches_prj_cd(cls, v, values):
        prj_cd_yr = yr_to_year(values.get("slug", "")[6:8])
        date_yr = str(v.year)
        if prj_cd_yr != date_yr:
            err_msg = f"""Year of end date (ssn_date1={v}) is not consistent with prj_cd ({prj_cd_yr})."""
            raise ValueError(err_msg)
        return v

    @validator("ssn_date1")
    def ssn_date0_before_ssn_date1(cls, v, values):
        ssn_date0 = values.get("ssn_date0")
        if ssn_date0 > v:
            raise ValueError(
                f"Season end date (ssn_date1={v}) occurs before start date(ssn_date0={ssn_date0})."
            )
        return v
