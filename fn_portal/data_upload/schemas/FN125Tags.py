from enum import Enum, IntEnum
from typing import Optional

from pydantic import constr, validator, PositiveInt
from .FNBase import FNBase
from .utils import string_to_int


class TagStatEnum(str, Enum):
    on_capture = "C"
    tag_applied = "A"


class XTaginckdEnum(IntEnum):

    no_tag = 0
    decoded = 1
    tag_lost = 2
    tag_unreadable = 3
    unknown = 9


# tag id must be populated unless tagdoc is like 6*

# if tagdoc is like 6*
# then xtaginckd must be one of 0, 1, 2, 3, or 9
# if tagdoc is like 6* and tagid is null  xtaginchk must be one of 0,  2, 3, or 9
# if tagdoc is like 6* and tagid is no null  xtaginchk must be  1


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
