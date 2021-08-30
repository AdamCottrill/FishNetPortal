from typing import Optional, Union

from pydantic import PositiveInt, validator

from .utils import EmptyStrToNone
from .FNBase import FNBase


class FN013(FNBase):

    gr: str
    gr_des: Optional[str]
    effcnt: Union[None, PositiveInt, EmptyStrToNone]
    effdst: Union[None, PositiveInt, EmptyStrToNone]

    # _gr_des_titlecase = validator("gr_des", allow_reuse=True)(to_titlecase)
    class Config:
        validate_assignment = True

    @validator("gr_des")
    def set_gr_des(cls, gr_des):
        if gr_des:
            return gr_des.title()
        else:
            return "Not Specified"
