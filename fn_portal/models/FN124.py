from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN123 import FN123


class FN124(FNPortalBaseModel):
    """
    a table for catch tallies.
    """

    id = models.AutoField(primary_key=True)

    catch = models.ForeignKey(
        FN123, related_name="length_tallies", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    siz = models.PositiveIntegerField()
    sizcnt = models.PositiveIntegerField()

    class Meta:
        ordering = ["catch", "siz"]
        unique_together = ("catch", "siz")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN124, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.catch, self.siz)
