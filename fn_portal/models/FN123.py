from common.models import Species
from django.contrib.gis.db import models
from django.template.defaultfilters import slugify


from .FN122 import FN122
from .BaseModel import FNPortalBaseModel


class FN123(FNPortalBaseModel):
    """
    a table for catch counts.
    """

    id = models.AutoField(primary_key=True)

    effort = models.ForeignKey(FN122, related_name="catch", on_delete=models.CASCADE)
    species = models.ForeignKey(
        Species, related_name="fn_catch_counts", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    grp = models.CharField(max_length=3, default="00", db_index=True)
    catcnt = models.IntegerField("Total Catch (numbers)", blank=True, null=True)
    count_only = models.IntegerField(
        "Fish counted but not sampled", blank=True, null=True
    )
    catwt = models.FloatField("Total Catch Weight (kg)", blank=True, null=True)
    biocnt = models.IntegerField(
        "Number of fish bio-sampled", default=0, blank=True, null=True
    )
    subcnt = models.IntegerField("Number of Fish in Subsample", blank=True, null=True)
    subwt = models.FloatField("Subsample Weight (kg)", blank=True, null=True)

    comment3 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("effort", "species", "grp")
        unique_together = ("effort", "species", "grp")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        self.biocnt = self.fish.count()
        super(FN123, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}-{}".format(self.effort, self.species.spc, self.grp)
