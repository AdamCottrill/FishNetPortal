from common.models import Vessel
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121

VESSEL_DIRECTION_CHOICES = [
    (0, "Variable"),
    (1, "Northeast"),
    (2, "East"),
    (3, "Southeast"),
    (4, "South"),
    (5, "Southwest"),
    (6, "West"),
    (7, "Northwest"),
    (8, "North"),
    (9, "Not Definable"),
]


class FN121Trawl(FNPortalBaseModel):
    """A table to hold information that is specific to trawl
    samples. THis table is an optional one-to-one relationshop with
    samples (FN121).

    """

    slug = models.SlugField(max_length=100, unique=True)

    sample = models.OneToOneField(
        FN121,
        related_name="trawl_data",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    vessel = models.ForeignKey(
        Vessel, related_name="trawl_samples", on_delete=models.CASCADE
    )

    vessel_speed = models.FloatField(
        "The speed of the research vessel (knots) during the sample.",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )

    vessel_direction = models.IntegerField(
        "The direction the vessel was traveling during the sample",
        choices=VESSEL_DIRECTION_CHOICES,
        blank=True,
        null=True,
    )

    warp = models.FloatField(
        "Trawl Gear Warp (tow line) Length expressed in meters (m).",
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record - this will be
        same as FN121, but include -trawl suffix."""
        return "{}-trawl".format(self.sample.slug)

    def save(self, *args, **kwargs):
        """when we save the object, make sure that our slug is populated."""

        self.slug = slugify(self.fishnet_keys())

        self.full_clean()

        super(FN121Trawl, self).save(*args, **kwargs)

        return self
