from typing import Optional
from enum import Enum
from pydantic import confloat, validator, constr

from .FNBase import FNBase
from .utils import string_to_float

xwind_regex = r"000|\d{3}-\d{2}"
xweather_regex = r"[1-4]{2}"


class PrecipEnum(str, Enum):

    none = "00"
    mist = "10"
    fog = "40"
    slight_drizzle = "51"
    heavy_drizzle = "55"
    light_rain = "61"
    heavy_rain = "65"
    light_snow = "71"
    heavy_snow = "75"
    light_rain_shower = "80"
    heavy_rain_shower = "85"
    thunder_storm = "95"


class FN121Weather(FNBase):
    """A pydandic schema model to validate FN121Weather objects.  slug
    and sample_id are required, the other fields represent weather
    condition data. They can be null, but must be constrained to
    plausible values.

    """

    slug: str
    sample_id: int

    airtem0: Optional[confloat(ge=-30, le=45)] = None
    airtem1: Optional[confloat(ge=-30, le=45)] = None
    cloud_pc0: Optional[confloat(ge=0, le=100)] = None
    cloud_pc1: Optional[confloat(ge=0, le=100)] = None
    waveht0: Optional[confloat(ge=0, le=3)] = None
    waveht1: Optional[confloat(ge=0, le=3)] = None

    # precip enum
    precip0: Optional[PrecipEnum] = None
    precip1: Optional[PrecipEnum] = None

    # XWIND_REGEX
    xwind0: Optional[constr(regex=xwind_regex)]
    xwind1: Optional[constr(regex=xwind_regex)]

    # XWEATHER_REGEX
    xweather: Optional[constr(regex=xweather_regex)]

    class Config:
        validate_assignment = True

    _string_to_float = validator(
        "airtem0",
        "airtem1",
        "cloud_pc0",
        "cloud_pc1",
        "waveht0",
        "waveht1",
        allow_reuse=True,
        pre=True,
    )(string_to_float)
