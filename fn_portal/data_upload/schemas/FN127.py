from enum import Enum
from typing import Optional

from pydantic import constr, conint, validator
from .FNBase import FNBase
from .utils import string_to_int


class EdgeEnum(str, Enum):

    omega = "o"
    asterisk = "*"
    plus = "+"
    plus_plus = "++"
    regenerated = "R"
    omega_x = "ox"
    check_zone = "x"
    omega_slash = "o/"


class FN127(FNBase):
    """Pydantic model for age estimates.

    Like FN125tags - this model should be updated  when we refactor the FN127 model into separte fields.

    TODO: Add additional constrains on agemt and xagem.

    """

    slug: str
    fish_id: int
    ageid: int
    preferred: bool
    agea: Optional[conint(ge=0)] = None
    xagem: constr(regex="^([A-Z0-9]{2})$", max_length=2)
    agemt: constr(regex="^([A-Z0-9]{5})$", max_length=5)
    edge: Optional[EdgeEnum] = None
    conf: Optional[conint(ge=1, le=9)] = None
    nca: Optional[conint(ge=0)] = None
    comment7: Optional[str]

    _string_to_int = validator("agea", "conf", "nca", allow_reuse=True, pre=True)(
        string_to_int
    )

    @validator("xagem")
    @classmethod
    def check_xagem_structure(cls, value, values):
        if value is not None:
            allowed = "01234567ABCDEFGMK"
            structure = value[1]
            if structure not in allowed:
                msg = f"Unknown aging structure ({','.join(structure)}) found in xagem ({value})"
                raise ValueError(msg)
        return value

    @validator("agemt")
    @classmethod
    def check_agemt_structure(cls, value, values):
        if value is not None:
            allowed = "01234567ABCDEFGMKT"
            structure = value[0]
            if structure not in allowed:
                msg = f"Unknown aging structure ({','.join(structure)}) found in agemt ({value})"
                raise ValueError(msg)
        return value

    @validator("agemt")
    @classmethod
    def check_agemt_prep1(cls, value, values):
        if value is not None:
            allowed = "012345679KT"
            prep = value[1]
            if prep not in allowed:
                msg = f"Unknown aging prep1 method ({','.join(prep)}) found in agemt ({value})"
                raise ValueError(msg)
        return value

    @validator("agemt")
    @classmethod
    def check_agemt_prep2(cls, value, values):
        if value is not None:
            allowed = "12349"
            prep = value[2]
            if prep not in allowed:
                slug = values["slug"]
                msg = f"Unknown aging prep2 method ({','.join(prep)}) found in agemt ({value})"
                raise ValueError(msg)
        return value
