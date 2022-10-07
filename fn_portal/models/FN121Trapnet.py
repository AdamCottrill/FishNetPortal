from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from common.models import BottomType, CoverType

from .BaseModel import FNPortalBaseModel
from .choices import VEGETATION_CHOICES

from .FN121 import FN121


class FN121Trapnet(FNPortalBaseModel):
    """A table to hold data that is specific to trap/hoopnet type gear.
    Optional one-to-onerelationshop with samples (FN121).

    """

    slug = models.SlugField(max_length=100, unique=True)

    sample = models.OneToOneField(
        FN121,
        related_name="trapnet_data",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    bottom = models.ForeignKey(
        # "Type of bottom (substrate) at a site or within an area of a waterbody.",
        BottomType,
        related_name="samples",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    cover = models.ForeignKey(
        # "Type of cover (vertical structure) available to fish at a sampling site.",
        CoverType,
        related_name="samples",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    vegetation = models.IntegerField(
        "Observed aquatic vegetation density.",
        choices=VEGETATION_CHOICES,
        blank=True,
        null=True,
    )

    lead_angle = models.FloatField(
        "The angle that gear was set relative to the shoreline",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(90)],
    )
    leaduse = models.FloatField(
        "Length of leader in the water (m)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )

    distoff = models.FloatField(
        "The distance between the shore and the start of the lead",
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        """when we save the object, make sure that our slug is populated."""

        self.slug = slugify(self.fishnet_keys())

        self.full_clean()
        super(FN121Trapnet, self).save(*args, **kwargs)

        return self

    def fishnet_keys(self):
        """return the fish-net II key fields for this record - this will be
        same as FN121, but include -trapnet suffix."""
        return "{}-trapnet".format(self.sample.slug)
