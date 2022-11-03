from enum import Enum
from typing import Optional

from pydantic import conint, constr, validator

from .FNBase import FNBase
from .utils import empty_to_none, string_to_int


def FN127Factory(agest_choices, ageprep1_choices, ageprep2_choices):
    """A factory function for a pydantic FN127 schema that includes
    current choices for agest, ageprep1 and ageprep2."""

    class EdgeEnum(str, Enum):

        omega = "o"
        asterisk = "*"
        plus = "+"
        plus_plus = "++"
        regenerated = "R"
        omega_x = "ox"
        check_zone = "x"
        omega_slash = "o/"

    class AgeFailEnum(str, Enum):

        no_structure = "91"
        regenerated_crystalized = "92"
        poorly_prepared = "93"
        contaminated_sample = "94"
        poor_structure = "95"

    class FN127(FNBase):
        """Pydantic model for age estimates.

        Like FN125tags - this model should be updated when we refactor the
        FN127 model into separate fields.

        """

        slug: str
        fish_id: int
        ageid: int
        preferred: bool
        agea: Optional[conint(ge=0)] = None

        agemt: constr(regex="^([A-Z0-9]{5})$", max_length=5)
        edge: Optional[EdgeEnum] = None
        conf: Optional[conint(ge=1, le=9)] = None
        nca: Optional[conint(ge=0)] = None

        agestrm: Optional[conint(ge=0)] = None
        agelake: Optional[conint(ge=0)] = None
        spawnchkcnt: Optional[conint(ge=0)] = None
        age_fail: Optional[AgeFailEnum] = None

        comment7: Optional[str]

        _string_to_int = validator("agea", "conf", "nca", allow_reuse=True, pre=True)(
            string_to_int
        )

        _empty_to_none = validator("edge", allow_reuse=True, pre=True)(empty_to_none)

        @validator("agemt", allow_reuse=True)
        @classmethod
        def check_agemt_structure(cls, value, values):
            if value is not None:
                structure = value[0]
                if structure not in agest_choices:
                    msg = f"Unknown aging structure ({','.join(structure)}) found in agemt ({value})"
                    raise ValueError(msg)
            return value

        @validator("agemt", allow_reuse=True)
        @classmethod
        def check_agemt_prep1(cls, value, values):
            if value is not None:
                prep = value[1]
                if prep not in ageprep1_choices:
                    msg = f"Unknown aging prep1 method ({','.join(prep)}) found in agemt ({value})"
                    raise ValueError(msg)
            return value

        @validator("agemt", allow_reuse=True)
        @classmethod
        def check_agemt_prep2(cls, value, values):
            if value is not None:
                prep = value[2]
                if prep not in ageprep2_choices:
                    msg = f"Unknown aging prep2 method ({','.join(prep)}) found in agemt ({value})"
                    raise ValueError(msg)
            return value

    return FN127
