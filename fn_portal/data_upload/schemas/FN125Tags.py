from enum import Enum, IntEnum
from typing import Optional


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


def FN125TagsFactory(
    tag_type_choices, tag_position_choices, tag_agency_choices, tag_colour_choices
):
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
        tagdoc: constr(
            regex="^([A-Z0-9]{5})$", to_upper=True, min_length=5, max_length=5
        )
        tagstat: TagStatEnum = "A"
        cwtseq: Optional[PositiveInt] = None

        comment_tag: Optional[str]

        _string_to_int = validator("cwtseq", allow_reuse=True, pre=True)(string_to_int)

        @validator("tagstat", allow_reuse=True)
        @classmethod
        def check_tagstat_n(cls, value, values):
            """Tag stat N (checked and not found) is only appropriate for pit or cwts."""
            tagdoc = values.get("tagdoc")
            if tagdoc and value == "N":
                if tagdoc[0] not in ["P", "6"]:
                    msg = (
                        "TAGSTAT='N' is only allowed if TAGTYPE is 6 (CWT) or P (PIT)."
                    )
                    raise ValueError(msg)
            return value

        @validator("tagstat", allow_reuse=True)
        @classmethod
        def check_null_tagid_if_tagstat_n(cls, value, values):
            """If tag stat is 'N' - tagid must be null. If you have a
            tagid, the tag was either applied or present on capture."""
            tagid = values["tagid"]
            if tagid and value == "N":
                msg = f"TAGSTAT cannot be 'N' if TAGID is populated (TAGID='{tagid}')."
                raise ValueError(msg)
            return value

        @validator("tagstat", allow_reuse=True)
        @classmethod
        def check_null_tagid_if_tagstat_a(cls, value, values):
            """If tag stat is 'N' - tagid must be null. If you have a
            tagid, the tag was either applied or present on capture."""
            tagid = values["tagid"]
            if tagid is None and value == "A":
                msg = f"TAGID cannot be empty if TAGSTAT='A' (tag applied)."
                raise ValueError(msg)
            return value

        @validator("tagdoc", allow_reuse=True)
        @classmethod
        def check_tag_type(cls, value, values):
            if value is not None:
                tag_type = value[0]
                if tag_type not in tag_type_choices:
                    msg = (
                        f"Unknown tag_type code ({tag_type}) found in TAGDOC ({value})"
                    )
                    raise ValueError(msg)
            return value

        @validator("tagdoc", allow_reuse=True)
        @classmethod
        def check_tag_position(cls, value, values):
            if value is not None:
                tag_position = value[1]
                if tag_position not in tag_position_choices:
                    msg = f"Unknown tag_position code ({tag_position}) found in TAGDOC ({value})"
                    raise ValueError(msg)
            return value

        @validator("tagdoc", allow_reuse=True)
        @classmethod
        def check_tag_agency(cls, value, values):
            if value is not None:
                agency = value[2:4]
                if agency not in tag_agency_choices:
                    msg = (
                        f"Unknown tag_agency code ({agency}) found in TAGDOC ({value})"
                    )
                    raise ValueError(msg)
            return value

        @validator("tagdoc", allow_reuse=True)
        @classmethod
        def check_tag_colour(cls, value, values):
            if value is not None:
                tag_colour = value[4]
                if tag_colour not in tag_colour_choices:
                    msg = f"Unknown tag_colour code ({tag_colour}) found in TAGDOC ({value})"
                    raise ValueError(msg)
            return value

    return FN125Tags
