from datetime import date
from enum import Enum
from pydantic import validator, constr, confloat, conint

from .utils import not_specified, to_uppercase, yr_to_year
from .FNBase import FNBase

GRP_REGEX = "^([A-Z0-9]{1,2})$"
FDSAM_REGEX = "^(0|[12][1-3])$"
SPCMRK_REGEX = "^(0|[1-3][0-2])$"
AGEDEC_REGEX = "^(0|[1234567ABCDEFGMTVX][01])$"


class BioSamEnum(str, Enum):
    NotSampled = "0"
    CompleteSampling = "1"
    RandomSampling = "2"
    SizeStratifiedSampling = "3"


class SizSamEnum(str, Enum):

    NotSampled = "0"
    FN125 = "1"
    FN124 = "2"
    BothFN124andFN125 = "3"


class SizAttEnum(str, Enum):

    FLEN = "flen"
    TLEN = "tlen"


class FN012(FNBase):
    """ """

    slug: str
    project_id: int

    species_id: int

    grp: constr(regex=GRP_REGEX, max_length=2)

    grp_des: str
    biosam: BioSamEnum
    sizsam: SizSamEnum
    sizatt: SizAttEnum
    sizint: conint(ge=1, le=50)

    fdsam: constr(regex=FDSAM_REGEX, max_length=2)
    spcmrk: constr(regex=SPCMRK_REGEX, max_length=2)
    agedec: constr(regex=AGEDEC_REGEX, max_length=2)

    flen_min: confloat(gt=0, lt=700)
    flen_max: confloat(gt=0, lt=2000)
    tlen_min: confloat(gt=0, lt=700)
    tlen_max: confloat(gt=0, lt=2000)
    rwt_min: confloat(gt=0, lt=5000)
    rwt_max: confloat(gt=0, lt=5000)
    k_min_error: confloat(gt=0, lt=2.0)
    k_min_warn: confloat(gt=0, lt=1.5)
    k_max_error: confloat(gt=0, lt=5.0)
    k_max_warn: confloat(gt=0, lt=4.0)
