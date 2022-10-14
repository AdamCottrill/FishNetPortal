from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121


class FN122(FNPortalBaseModel):
    """
    A table to hold information about individual fishing
    efforts(mesh/panel attributes)

    """

    id = models.AutoField(primary_key=True)

    sample = models.ForeignKey(FN121, related_name="effort", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    # sam = models.CharField(max_length=5, blank=True, null=True)
    eff = models.CharField(max_length=4, db_index=True, default=1)
    effdst = models.FloatField(blank=True, null=True)
    grdep0 = models.FloatField(blank=True, null=True)
    grdep1 = models.FloatField(blank=True, null=True)
    grtem0 = models.FloatField(blank=True, null=True)
    grtem1 = models.FloatField(blank=True, null=True)
    waterhaul = models.BooleanField(default=False)
    efftm0 = models.TimeField("Effort Start Date", blank=True, null=True, db_index=True)
    efftm1 = models.TimeField("Effort End Time", blank=True, null=True, db_index=True)
    comment2 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("sample", "eff")
        unique_together = ("sample", "eff")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN122, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.sample, self.eff)
