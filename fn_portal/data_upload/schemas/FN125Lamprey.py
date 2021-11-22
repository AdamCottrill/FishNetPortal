from enum import Enum
from typing import Optional

from pydantic import constr, conint, root_validator, validator
from .FNBase import FNBase
from .utils import empty_to_none


class LamIjcEnum(str, Enum):
    NoWound = "0"
    A1 = "A1"
    A2 = "A2"
    A3 = "A3"
    A4 = "A4"
    B1 = "B1"
    B2 = "B2"
    B3 = "B3"
    B4 = "B4"


class FN125Lamprey(FNBase):
    """Pydantic model for Lamprey wounds.

    The lamijc_regex is a 0 OR an A or a B follwed by a number between
    1 and 4 optionally followed by two digits between 10 and 50.

    """

    slug: str
    fish_id: int
    lamid: str
    xlam: Optional[constr(regex=r"^0|\d{4}$")]
    lamijc_type: Optional[LamIjcEnum]
    lamijc_size: Optional[conint(ge=10)]
    comment_lam: Optional[str]

    # need to have either xlam or lamijc should not have both.

    _empty_to_none = validator(
        "xlam",
        "lamijc_type",
        "lamijc_size",
        "comment_lam",
        allow_reuse=True,
        pre=True,
    )(empty_to_none)

    @root_validator(pre=True)
    @classmethod
    def check_xlam_or_lamijc(cls, values):
        """Make sure there is either an xlam or lamicj value defined - but not both"""

        xlam = values.get("xlam")
        lamijc_type = values.get("lamijc_type")
        if lamijc_type is None and xlam is None:
            msg = f"No wounding information found in record."
            raise ValueError(msg)
        if lamijc_type and xlam:

            msg = f"Two different wound reporting mechanisms used."
            raise ValueError(msg)
        return values
