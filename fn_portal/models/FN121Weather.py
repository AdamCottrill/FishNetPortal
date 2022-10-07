from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .BaseModel import FNPortalBaseModel
from .choices import PRECIP_CHOICES, PRECIP_DURAITON_CHOICES, WAVE_DURAITON_CHOICES
from .FN121 import FN121


class FN121Weather(FNPortalBaseModel):
    """A table to hold weather/environmental data that is occationally
    collected during a sample.  Optional one-to-onerelationshop with
    samples (FN121).

    """

    slug = models.SlugField(max_length=100, unique=True)

    sample = models.OneToOneField(
        FN121,
        related_name="weather_data",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    airtem0 = models.FloatField(
        "Air temperature (C) at the sampling site at the time when sampling starts",
        blank=True,
        null=True,
        validators=[MinValueValidator(-30), MaxValueValidator(45)],
    )

    airtem1 = models.FloatField(
        "Air temperature (C) at the sampling site at the time when sampling ends",
        blank=True,
        null=True,
        validators=[MinValueValidator(-30), MaxValueValidator(45)],
    )

    wind_speed0 = models.IntegerField(
        "Wind wind speed in knots at the time when sampling starts.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    wind_speed1 = models.IntegerField(
        "Wind wind speed in knots at the time when sampling ends.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    wind_direction0 = models.IntegerField(
        "Wind wind direction in degrees at the time when sampling starts.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
    )

    wind_direction1 = models.IntegerField(
        "Wind wind direction in degrees at the time when sampling ends.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(360)],
    )

    precip0 = models.CharField(
        "The type of precipitation, fog or mist the time when sampling starts.",
        max_length=2,
        choices=PRECIP_CHOICES,
        blank=True,
        null=True,
    )

    precip1 = models.CharField(
        "The type of precipitation, fog or mist the time when sampling ends.",
        max_length=2,
        choices=PRECIP_CHOICES,
        blank=True,
        null=True,
    )

    cloud_pc0 = models.FloatField(
        "Cloud cover, expressed as a percent at the time when sampling starts.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    cloud_pc1 = models.FloatField(
        "Cloud cover, expressed as a percent at the time when sampling ends.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    waveht0 = models.FloatField(
        "Wave height measured in meters (m) at the time when sampling starts.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )

    waveht1 = models.FloatField(
        "Wave height measured in meters (m) at the time when sampling ends.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(3)],
    )

    # FN121_Weather.XWEATHER
    precip_duration = models.IntegerField(
        "duration of precipitation for the set",
        choices=PRECIP_DURAITON_CHOICES,
        blank=True,
        null=True,
    )

    wave_duration = models.IntegerField(
        "duration of waves for the set",
        choices=WAVE_DURAITON_CHOICES,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug.upper()

    @property
    def wind0(self):
        """FN-II defined wind as compound field comprised to two parts
        - wind direction and speeed.  This method provides a wind
        property to our model that emulates the original string
        format.

        """
        if self.wind_speed0 == 0 and self.wind_direction0 == 0:
            return "000"
        elif self.wind_speed0 is None and self.wind_direction0 is None:
            return None
        else:
            return f"{self.wind_direction0:03}-{self.wind_speed0:02}"

    @property
    def wind1(self):
        """FN-II defined wind as compound field comprised to two parts
        - wind direction and speeed.  This method provides a wind
        property to our model that emulates the original string
        format.

        """
        if self.wind_speed1 == 0 and self.wind_direction1 == 0:
            return "000"
        elif self.wind_speed1 is None and self.wind_direction1 is None:
            return None
        else:
            return f"{self.wind_direction1:03}-{self.wind_speed1:02}"

    @property
    def xweather(self):
        """FN-II defined xweather as compound field comprised to two
        parts - precip duration and wave duration.  THis method
        provides an xweather property to our model that emulates the
        original string format.

        """
        if not self.precip_duration and not self.wave_duration:
            return None
        else:
            return f"{self.precip_duration}{self.wave_duration}"

    def clean(self):
        """The wind_direction and wind_speed form a complimentary
        pair.  We cannot have one wiout the other and if one is 0, the
        other must be 0.

        """

        if self.precip_duration and self.wave_duration is None:
            msg = "wave_duration cannot be null if precip_duration is provided."
            raise ValidationError(_(msg))
        if self.precip_duration is None and self.wave_duration:
            msg = "precip_duration cannot be null if wave_duration is provided."
            raise ValidationError(_(msg))

        if self.wind_direction0 and self.wind_speed0 is None:
            msg = "wind_speed0 cannot be null if wind_direction0 is provided."
            raise ValidationError(_(msg))
        if self.wind_direction0 is None and self.wind_speed0:
            msg = "wind_direction0 cannot be null if wind_speed0 is provided."
            raise ValidationError(_(msg))
        if self.wind_direction1 and self.wind_speed1 is None:
            msg = "wind_speed1 cannot be null if wind_direction1 is provided."
            raise ValidationError(_(msg))
        if self.wind_direction1 is None and self.wind_speed1:
            msg = "wind_direction1 cannot be null if wind_speed1 is provided."
            raise ValidationError(_(msg))

        if (self.wind_direction0 == 0 and self.wind_speed0 != 0) or (
            self.wind_direction0 != 0 and self.wind_speed0 == 0
        ):
            msg = (
                "wind_direction0 and wind_speed0 must both be 0 if " "one of them is 0."
            )
            raise ValidationError(_(msg))
        if (self.wind_direction1 == 0 and self.wind_speed1 != 0) or (
            self.wind_direction1 != 0 and self.wind_speed1 == 0
        ):
            msg = (
                "wind_direction1 and wind_speed1 must both be 0 if " "one of them is 0."
            )
            raise ValidationError(_(msg))

    def save(self, *args, **kwargs):
        """when we save the object, make sure that our slug is
        populated, and our validators are run with self.full_clean()"""

        self.slug = slugify(self.fishnet_keys())

        self.full_clean()
        super(FN121Weather, self).save(*args, **kwargs)

        return self

    def fishnet_keys(self):
        """return the fish-net II key fields for this record - this will be
        same as FN121, but include -weather suffix."""
        return "{}-weather".format(self.sample.slug)
