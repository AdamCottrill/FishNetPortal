from typing import Optional

from pydantic import conint, validator

from .FNBase import FNBase
from .utils import string_to_int


class FN123NonFish(FNBase):
    """Pydantic model for Catch Counts of things that are not
    fish. (turtles and burds.).

    Catcnt if present must be more than 1.  If mortcnt is populated,
    it must be less than catcnt.

    """

    slug: str
    effort_id: int
    taxon_id: int

    catcnt: Optional[conint(ge=1)] = None
    mortcnt: Optional[conint(ge=0)] = None
    comment3: Optional[str]

    _string_to_int = validator("catcnt", "mortcnt", allow_reuse=True, pre=True)(
        string_to_int
    )

    @validator("mortcnt")
    def check_catcnt_vs_mortcnt(cls, v, values):
        catcnt = values.get("catcnt")
        if catcnt is not None and v is not None:
            if catcnt < v:
                msg = f"MORTCNT ({v}) cannot be greater than CATCNT ({catcnt})"
                raise ValueError(msg)
