from typing import Optional
from enum import Enum
from pydantic import confloat, conint, validator

from .FNBase import FNBase
from .utils import string_to_float, string_to_int


def FN121ElectroFishingFactory(waveform_choices):
    """A factory fucntion that will return a pydandic validator class
    that includes current valid waveform type choices.

    Arguments:
    - `agest_choices`:

    """

    WaveFormEnum = Enum("WaveFormEnum", waveform_choices)

    class FN121ElectroFishing(FNBase):
        """A pydandic schema model to validate FN121Electrofishing
        objects.  slug and sample_id are required, the other fields
        represent electrofishing attributes, settings, and relevant
        environmental data. Generally, they can be null, but mist be
        constrained to plausible values.

        """

        slug: str
        sample_id: int

        shock_sec: Optional[conint(ge=0, le=3000)] = None
        volts_min: Optional[confloat(ge=0, le=1200)] = None
        volts_max: Optional[confloat(ge=0, le=1200)] = None
        volts_mean: Optional[confloat(ge=0, le=1200)] = None
        amps_min: Optional[confloat(ge=0, le=80)] = None
        amps_max: Optional[confloat(ge=0, le=80)] = None
        amps_mean: Optional[confloat(ge=0, le=80)] = None
        power_min: Optional[confloat(ge=0, le=15000)] = None
        power_max: Optional[confloat(ge=0, le=15000)] = None
        power_mean: Optional[confloat(ge=0, le=15000)] = None
        conduct: Optional[confloat(ge=0, le=2000)] = None
        turbidity: Optional[confloat(ge=0, le=400)] = None
        freq: Optional[conint(ge=10, le=250)] = None
        pulse_dur: Optional[confloat(ge=0)] = None
        pulse_pattern: Optional[str]
        duty_cycle: Optional[confloat(ge=0, le=100)] = None
        waveform: Optional[WaveFormEnum]
        anodes: Optional[conint(ge=1, le=2)] = None
        num_netters: Optional[conint(ge=0, le=8)] = None
        comment: Optional[str]

        class Config:
            validate_assignment = True

        _string_to_float = validator(
            "volts_min",
            "volts_max",
            "volts_mean",
            "amps_min",
            "amps_max",
            "amps_mean",
            "power_min",
            "power_max",
            "power_mean",
            "conduct",
            "turbidity",
            "pulse_dur",
            "duty_cycle",
            allow_reuse=True,
            pre=True,
        )(string_to_float)

        _string_to_int = validator(
            "shock_sec",
            "freq",
            "anodes",
            "num_netters",
            allow_reuse=True,
            pre=True,
        )(string_to_int)

    return FN121ElectroFishing
