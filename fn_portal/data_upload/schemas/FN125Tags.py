from enum import Enum, IntEnum
from typing import Optional
from django.db.models.query import prefetch_related_objects

from pydantic import constr, validator, PositiveInt
from .FNBase import FNBase
from .utils import string_to_int


class TagStatEnum(str, Enum):
    on_capture = "C"
    tag_applied = "A"
    no_tag = "N"


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
    tagid: Optional[str]
    tagdoc: constr(regex="^([A-Z0-9]{5})$", min_length=5, max_length=5)
    tagstat: TagStatEnum = "A"
    cwtseq: Optional[PositiveInt] = None

    comment_tag: Optional[str]

    _string_to_int = validator("cwtseq", allow_reuse=True, pre=True)(string_to_int)

    @validator("tagstat")
    @classmethod
    def check_tagstat_n(cls, value, values):
        """Tag stat N (checked and not found) is only appropriate for pit or cwts."""
        tagdoc = values.get("tagdoc")
        if tagdoc and value == "N":
            if tagdoc[0] not in ["P", "6"]:
                msg = "TAGSTAT='N' is only allowed if TAGTYPE is 6 (CWT) or P (PIT)."
                raise ValueError(msg)
        return value

    @validator("tagstat")
    @classmethod
    def check_null_tagid_if_tagstat_n(cls, value, values):
        """If tag stat is 'N' - tagid must be null. If you have a
        tagid, the tag was either applied or present on capture."""
        tagid = values["tagid"]
        if tagid and value == "N":
            msg = f"TAGSTAT cannot be 'N' if TAGID is populated (TAGID='{tagid}')."
            raise ValueError(msg)
        return value

    @validator("tagstat")
    @classmethod
    def check_null_tagid_if_tagstat_a(cls, value, values):
        """If tag stat is 'N' - tagid must be null. If you have a
        tagid, the tag was either applied or present on capture."""
        tagid = values["tagid"]
        if tagid is None and value == "A":
            msg = f"TAGID cannot be empty if TAGSTAT='A' (tag applied)."
            raise ValueError(msg)
        return value
