from django.contrib.gis.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.urls import reverse

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121


class FN121Limno(FNPortalBaseModel):
    """A table to hold limnologilal (water chemistry) attributes
    associated with a single net set.  Optional one-to-one
    relationshop with samples (FN121).

    """

    slug = models.SlugField(max_length=100, unique=True)

    sample = models.OneToOneField(
        FN121,
        related_name="fn121_sample",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    do_gear = models.FloatField(
        "Dissolved Oxygen (mg/l) at Gear",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    xo2 = models.FloatField(
        "Bottom Dissolved Oxygen (mg/l) [start]",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    xo22 = models.FloatField(
        "Bottom Dissolved Oxygen (mg/l)  [end]",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    surfdo2 = models.FloatField(
        "Surface Dissolved Oxygen (mg/l)  [start]",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )
    surfdo22 = models.FloatField(
        "Surface Dissolved Oxygen (mg/l) [end]",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(20)],
    )

    class Meta:
        ordering = ["slug"]

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        """when we save the object, make sure that our slug is populated."""

        self.slug = slugify(self.fishnet_keys())

        self.full_clean()
        super(FN121Limno, self).save(*args, **kwargs)

        return self

    def fishnet_keys(self):
        """return the fish-net II key fields for this record - this will be
        same as FN121, but include -limino suffix."""
        return "{}-limno".format(self.sample.slug)
