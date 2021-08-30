from typing import Optional, Union

from pydantic import PositiveFloat, PositiveInt, validator

from .utils import EmptyStrToNone
from .FNBase import FNBase


class FN014(FNBase):

    gr: str
    eff: str
    eff_des: str
    mesh: Union[None, PositiveInt, EmptyStrToNone]
    grlen: Union[None, PositiveFloat, EmptyStrToNone]
    grht: Union[None, PositiveFloat, EmptyStrToNone]
    grwid: Union[None, PositiveFloat, EmptyStrToNone]
    grcol: Optional[str]
    grmat: Optional[str]
    gryarn: Optional[str]
    grknot: Optional[str]

    # _eff_des_titlecase = validator("eff_des", allow_reuse=True)(to_titlecase)
    class Config:
        validate_assignment = True

    @validator("eff_des")
    def set_eff_des(cls, eff_des):
        if eff_des:
            return eff_des.title()
        else:
            return "Not Specified"
