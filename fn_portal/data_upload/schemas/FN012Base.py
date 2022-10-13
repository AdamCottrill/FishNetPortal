from datetime import date
from enum import Enum, IntEnum
from typing import Optional
from pydantic import validator, constr, confloat, conint

from .utils import to_uppercase, check_ascii_sort, check_agest
from .FNBase import FNBase

GRP_REGEX = "^([A-Z0-9]{1,2})$"
FDSAM_REGEX = "^(0|[12][1-3])$"
SPCMRK_REGEX = "^(0|[1-3][0-2])$"
AGEST_REGEX = "^(0|[1234567ABCDEFMTV]+)$"


class BioSamEnum(str, Enum):
    NotSampled = "0"
    CompleteSampling = "1"
    RandomSampling = "2"
    SizeStratifiedSampling = "3"


class SizSamEnum(IntEnum):

    NotSampled = 0
    FN125 = 1
    FN124 = 2
    BothFN124andFN125 = 3


class SizAttEnum(str, Enum):

    flen = "FLEN"
    tlen = "TLEN"


class LamSamEnum(str, Enum):

    NotSampled = "0"
    XLAM = "1"
    LAMIJC = "2"


class FN012Base(FNBase):
    """A pydantic validator that will be used to validate all of the
    common attributes associated with FN012 objects. Inherited by FN012
    and FN012Protocol validators."""

    slug: str

    species_id: int

    grp: constr(regex=GRP_REGEX, max_length=2)

    grp_des: str
    biosam: BioSamEnum
    sizsam: SizSamEnum
    sizatt: Optional[SizAttEnum] = None
    sizint: Optional[conint(ge=1, le=50)] = None
    lamsam: LamSamEnum

    fdsam: constr(regex=FDSAM_REGEX, max_length=2)
    spcmrk: constr(regex=SPCMRK_REGEX, max_length=2)

    agest: constr(regex=AGEST_REGEX, max_length=8)

    flen_min: Optional[confloat(gt=0, lt=700)]
    flen_max: Optional[confloat(gt=0, lt=2000)]
    tlen_min: Optional[confloat(gt=0, lt=700)]
    tlen_max: Optional[confloat(gt=0, lt=2000)]

    rwt_min: Optional[confloat(gt=0, lt=55000)]
    rwt_max: Optional[confloat(gt=0, lt=55000)]

    # make sure min is less than max
    # errors are more extreme than warn.

    # no max (lt)] on min values:
    k_min_error: Optional[confloat(ge=0.05, lt=5.0)]
    k_min_warn: Optional[confloat(ge=0.07, lt=4.0)]
    # no min (gt)] on max values:
    k_max_warn: Optional[confloat(ge=0.07, lt=4.0)]
    k_max_error: Optional[confloat(ge=0.05, lt=5.0)]

    _to_uppercase = validator("sizatt", "agest", allow_reuse=True, pre=True)(
        to_uppercase
    )

    @validator("sizint", allow_reuse=True)
    def check_sizint_if_sizsam(cls, v, values):
        sizsam = values.get("sizsam")
        if sizsam in (2, 3) and v is None:
            msg = f"SIZINT is required if SIZSAM is 2 or 3"
            raise ValueError(msg)
        return v

    @validator("sizatt", allow_reuse=True)
    def check_sizatt_if_sizsam(cls, v, values):
        sizsam = values.get("sizsam")
        if sizsam in (2, 3) and v is None:
            msg = f"SIZATT is required if SIZSAM is 2 or 3"
            raise ValueError(msg)
        return v

    @validator(
        "flen_min",
        "flen_max",
        "tlen_min",
        "tlen_max",
        "rwt_min",
        "rwt_max",
        "k_min_error",
        "k_min_warn",
        "k_max_warn",
        "k_max_error",
        allow_reuse=True,
    )
    def biosam_required_field(cls, v, values, field):
        biosam = values.get("biosam")

        if biosam != "0" and v is None:
            msg = f"{field.name} is required if BIOSAM='{biosam}'"
            raise ValueError(msg)
        return v

    _check_ascii_sort = validator("agest", allow_reuse=True)(check_ascii_sort)
    _check_agest = validator("agest", allow_reuse=True)(check_agest)
