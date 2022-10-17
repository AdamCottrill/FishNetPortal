from typing import Optional
from enum import Enum, IntEnum
from pydantic import conint, confloat, validator, constr

from .FNBase import FNBase
from .utils import (
    check_ascii_sort,
    string_to_int,
    string_to_float,
    to_uppercase,
    check_ascii_sort,
    check_agest,
)


class FateEnum(str, Enum):
    killed = "K"
    released = "R"


class SexEnum(IntEnum):
    male = 1
    female = 2
    hermaphrodite = 3
    unknown = 9


class MatEnum(IntEnum):
    immature = 1
    mature = 2
    unknown = 9


class StomFlagEnum(str, Enum):
    not_collected = "0"
    fn126_records = "1"
    external_database = "2"


# see the data dictionary for valid goncodes
gon_regex = r"(^[1-4|9]$)|(^([1-5]0)|(2[1-3])|(99))[2-8A-E]?$"


class FN125(FNBase):
    """Pydanic model for bioligical samples.

    most of the fieds in a biological sample are optional, but if they
    are provided, they are subject to constraints.

    """

    slug: str
    catch_id: int
    fish: int
    rwt: Optional[confloat(gt=0)] = None
    flen: Optional[conint(gt=0)] = None
    tlen: Optional[conint(gt=0)] = None
    girth: Optional[conint(gt=0)] = None
    sex: Optional[SexEnum]
    mat: Optional[MatEnum]
    gon: Optional[constr(regex=gon_regex)]
    clipc: Optional[str]
    clipa: Optional[str]
    nodc: Optional[str]
    noda: Optional[str]
    tissue: Optional[str]
    agest: Optional[str]
    fate: FateEnum = FateEnum.killed

    stom_flag: Optional[StomFlagEnum]

    comment5: Optional[str]

    class Config:
        validate_assignment = True

    _string_to_int = validator("tlen", "flen", "girth", allow_reuse=True, pre=True)(
        string_to_int
    )

    _string_to_float = validator("rwt", allow_reuse=True, pre=True)(string_to_float)

    _to_uppercase = validator(
        "agest", "tissue", "clipc", "clipa", allow_reuse=True, pre=True
    )(to_uppercase)

    _check_agest = validator("agest", allow_reuse=True)(check_agest)

    @validator("fate", pre=True)
    def set_fate(cls, fate):
        if fate:
            return fate
        else:
            return "K"

    @validator("tlen")
    @classmethod
    def check_flen_vs_tlen(cls, v, values):
        flen = values.get("flen")
        if flen is not None and v is not None:
            if flen > v:
                msg = f"TLEN ({v}) must be greater than or equal to FLEN ({flen})"
                raise ValueError(msg)
        return v

    @validator("tlen", "flen")
    @classmethod
    def check_condition(cls, v, values, **kwargs):
        """mininum of 0.1 for very, very, small smelt sampled in lake erie
        (lenght=41, rwt=0.1)"""
        rwt = values.get("rwt")
        if rwt is not None and v is not None:
            k = 100000 * rwt / (v**3)
            if k > 3.5:
                msg = f"FLEN/TLEN ({v}) is too short for the round weight (RWT={rwt}) (K={k:.3f})"
                raise ValueError(msg)
            if k < 0.1:
                msg = f"FLEN/TLEN ({v}) is too large for the round weight (RWT={rwt}) (K={k:.3f})"
                raise ValueError(msg)
        return v

    @validator("tissue")
    @classmethod
    def check_tissue(cls, value, values):
        if value is not None:
            allowed = "123456789ABCDEHKNV"
            unknown = [c for c in value if c not in allowed]
            if unknown:
                msg = f"Unknown tissue code ({','.join(unknown)}) found in TISSUE ({value})"
                raise ValueError(msg)
        return value

    @validator("clipc", "clipa")
    @classmethod
    def check_clic_codes(cls, value, values):
        if value is not None:
            allowed = "01234567ABCDEFG"
            unknown = [c for c in value if c not in allowed]
            if unknown:
                msg = f"Unknown clip code ({','.join(unknown)}) found in clipa/clipc ({value})"
                raise ValueError(msg)
        return value

    # ascii-sort clips, node, agest and tissue
    _check_ascii_sort = validator(
        "agest", "tissue", "clipc", "clipa", allow_reuse=True
    )(check_ascii_sort)
