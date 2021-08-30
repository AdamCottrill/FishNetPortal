from typing import Optional

from pydantic import constr, conint, confloat, validator
from .FNBase import FNBase
from .utils import string_to_int, string_to_float


class FN123(FNBase):
    """Pydantic model for FN123  - Catch Counts.

    slug, effort_id, and species_id are all required fields.  All
    other fields are currently optional. If catcnt is populated, it
    must be larger than both biocnt and subcnt.  If catwt is
    populated, it must be greater than subwt.

    """

    slug: str
    effort_id: int
    species_id: int

    grp: constr(regex="^([A-Z0-9]{1,2})$", max_length=2)

    catcnt: Optional[conint(ge=0)] = None
    biocnt: Optional[conint(ge=0)] = None
    catwt: Optional[confloat(ge=0)] = None
    subcnt: Optional[conint(ge=0)] = None
    subwt: Optional[confloat(ge=0)] = None
    comment3: Optional[str]

    _string_to_float = validator("catwt", "subwt", allow_reuse=True, pre=True)(
        string_to_float
    )

    _string_to_int = validator(
        "catcnt", "subcnt", "biocnt", allow_reuse=True, pre=True
    )(string_to_int)

    @validator("biocnt")
    def check_catcnt_vs_biocnt(cls, v, values):
        catcnt = values.get("catcnt")
        if catcnt is not None and v is not None:
            if catcnt < v:
                msg = f"BIOCNT ({v}) cannot be greater than CATCNT ({catcnt})"
                raise ValueError(msg)

    @validator("subcnt")
    def check_catcnt_vs_subcnt(cls, v, values):
        catcnt = values.get("catcnt")
        if catcnt is not None and v is not None:
            if catcnt < v:
                msg = f"SUBCNT ({v}) cannot be greater than CATCNT ({catcnt})"
                raise ValueError(msg)

    @validator("subwt")
    def check_catwt_vs_subwt(cls, v, values):
        catwt = values.get("catwt")
        if catwt is not None and v is not None:
            if catwt < v:
                msg = f"SUBWT ({v}) cannot be greater than CATWT ({catwt})"
                raise ValueError(msg)
