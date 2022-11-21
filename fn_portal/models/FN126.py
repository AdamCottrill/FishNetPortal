from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN125 import FN125


class FN126(FNPortalBaseModel):
    """A table for diet data collected in the field.

    The FN126 table is used to store data collected from diet analysis
    studies. The FOOD field, when combined with other primary key fields,
    is used to uniquely identify each record in the table. The FN126 table
    is unique in that there are two 'indication' fields used to validate
    whether a sample should be expected: the FDSAM field in the FN012
    table and the STOM_FLAG field in the FN125 table. The specific
    combinations of each indicator field and how they relate to the FN126
    table are indicated below.

    A species with FDSAM == 0 in the FN012 table must have STOM_FLAG
    == 0 in the FN125 table and no records in the FN126 table.

    A species with FDSAM == 1 in the FN012 table can have any
    STOM_FLAG value (0-2) in the FN125 table. If STOM_FLAG == 0 or
    STOM_FLAG == 1 no records should exist in the FN126 table. If
    STOM_FLAG == 2 a record must exist in the FN126 table.

    A species with FDSAM == 2 in the FN012 table can have any
    STOM_FLAG value (0-2) in the FN125 table. This FDSAM value
    indicates that diet data is stored outside of GLIS, so no records
    should exist in the FN126 table.

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
        ("00", "Multiple"),
        ("10", "Egg"),
        ("20", "Larvae/Nauplii"),
        ("30", "Pupa"),
        ("40", "Nymph"),
        ("50", "Juvenile/Adult"),
        ("60", "Remains"),
        ("99", "Unknown"),
    )

    lifestage = models.CharField(
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
