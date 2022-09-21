from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN125 import FN125


class FN125_Lamprey(FNPortalBaseModel):
    """
    a table for lamprey data.
    """

    id = models.AutoField(primary_key=True)

    fish = models.ForeignKey(
        FN125, related_name="lamprey_marks", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    lamid = models.IntegerField()
    xlam = models.CharField(max_length=6, blank=True, null=True)

    LAMIJC_TYPE_CHOICES = (
        ["0", "0"],
        ["a1", "A1"],
        ["a2", "A2"],
        ["a3", "A3"],
        ["a4", "A4"],
        ["b1", "B1"],
        ["b2", "B2"],
        ["b3", "B3"],
        ["b4", "B4"],
    )
    lamijc_type = models.CharField(
        max_length=2, choices=LAMIJC_TYPE_CHOICES, default="0"
    )

    lamijc_size = models.IntegerField(blank=True, null=True)
    comment_lam = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["slug", "lamid"]

    def __str__(self):

        if self.xlam:
            return "{} (xlam: {})".format(self.slug.upper(), self.xlam)
        else:
            return "{} (lamijc: {}{})".format(
                self.slug.upper(), self.lamijc_type, self.lamijc_size
            )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125_Lamprey, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.lamid)
