from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

from .FN125 import FN125
from .BaseModel import FNPortalBaseModel


class FN126(FNPortalBaseModel):
    """
    a table for diet data collected in the field.
    """

    id = models.AutoField(primary_key=True)

    fish = models.ForeignKey(FN125, related_name="diet_data", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    food = models.IntegerField("Food Id")
    taxon = models.CharField(
        "A taxonomic code used to identify the type of food item.",
        max_length=10,
        db_index=True,
        blank=True,
        null=True,
    )
    fdcnt = models.IntegerField("Food Count", blank=True, null=True)
    fdval = models.FloatField("Food Measure Value", blank=True, null=True)

    FDMES_CHOICES = (
        (None, "No Data"),
        ("L", "Length"),
        ("W", "Weight"),
        ("V", "Volume"),
    )
    fdmes = models.CharField(
        help_text="Food Measure Code",
        max_length=2,
        blank=True,
        null=True,
        choices=FDMES_CHOICES,
    )

    LIFESTAGE_CHOICES = (
        (None, "No Data"),
        ("10", "10"),
        ("20", "20"),
        ("30", "30"),
        ("40", "40"),
        ("50", "50"),
        ("60", "60"),
    )
    lf = models.CharField(
        help_text="Life Stage",
        max_length=2,
        blank=True,
        null=True,
        choices=LIFESTAGE_CHOICES,
    )

    comment6 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "food"]
        unique_together = ("fish", "food")

    def __str__(self):
        return "{} ({}: {})".format(self.slug.upper(), self.taxon, self.fdcnt)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN126, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.food)
