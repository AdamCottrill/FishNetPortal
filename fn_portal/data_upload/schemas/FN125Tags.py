from enum import Enum
from typing import Optional

from pydantic import constr, validator, PositiveInt
from .FNBase import FNBase
from .utils import string_to_int


class TagStatEnum(str, Enum):
    on_capture = "C"
    tag_applied = "A"


class FN125Tags(FNBase):
    """Pydantic model for fish tags.

    this model will be revisited after tag model is refactored -
    tagdoc needs to be split into distinct fields.  Similarly, attributes
    of tag on capture need to be split apart.

    """

    slug: str
    fish_id: int
    fish_tag_id: int
    tagid: str
    tagdoc: constr(regex="^([A-Z0-9]{5})$", min_length=5, max_length=5)
    tagstat: TagStatEnum = "A"
    xcwtseq: Optional[PositiveInt] = None
    xtaginckd: Optional[bool]
    comment_tag: Optional[str]

    _string_to_int = validator("xcwtseq", allow_reuse=True, pre=True)(string_to_int)
