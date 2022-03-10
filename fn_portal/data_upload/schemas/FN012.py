from datetime import date
from enum import Enum, IntEnum
from typing import Optional
from pydantic import validator, constr, confloat, conint

from .utils import not_specified, to_uppercase, yr_to_year
from .FNBase import FNBase

GRP_REGEX = "^([A-Z0-9]{1,2})$"
FDSAM_REGEX = "^(0|[12][1-3])$"
SPCMRK_REGEX = "^(0|[1-3][0-2])$"
AGEDEC_REGEX = "^(00?|[1234567ABCDEFGMTVX][01])$"


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


class FN012(FNBase):
    """ """

    slug: str
    project_id: int

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
    agedec: constr(regex=AGEDEC_REGEX, max_length=2)

    flen_min: confloat(gt=0, lt=700)
    flen_max: confloat(gt=0, lt=2000)
    tlen_min: confloat(gt=0, lt=700)
    tlen_max: confloat(gt=0, lt=2000)

    rwt_min: confloat(gt=0, lt=55000)
    rwt_max: confloat(gt=0, lt=55000)

    # make sure min is less than max
    # errors are more extreme than warn.

    # no max (lt) on min values:
    k_min_error: confloat(ge=0.05, lt=5.0)
    k_min_warn: confloat(ge=0.07, lt=4.0)
    # no min (gt) on max values:
    k_max_warn: confloat(ge=0.07, lt=4.0)
    k_max_error: confloat(ge=0.05, lt=5.0)

    _to_uppercase = validator("sizatt", allow_reuse=True, pre=True)(to_uppercase)

    @validator("sizint")
    def check_sizint_if_sizsam(cls, v, values):
        sizsam = values.get("sizsam")
        if sizsam in (2, 3) and v is None:
            msg = f"SIZINT is required if SIZSAM is 2 or 3"
            raise ValueError(msg)
        return v

    @validator("sizatt")
    def check_sizatt_if_sizsam(cls, v, values):
        sizsam = values.get("sizsam")
        if sizsam in (2, 3) and v is None:
            msg = f"SIZATT is required if SIZSAM is 2 or 3"
            raise ValueError(msg)
        return v
