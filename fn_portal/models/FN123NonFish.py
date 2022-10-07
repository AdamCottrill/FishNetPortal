from common.models import Taxon
from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN122 import FN122


class FN123NonFish(FNPortalBaseModel):
    """a table for catch count of animals that are not fish. Most
    often these catch counts include thinks like waterbirds, mammals
    (beavers or otters), and amphibians and reptiles.

    """

    id = models.AutoField(primary_key=True)

    effort = models.ForeignKey(
        FN122, related_name="non_fish_catch", on_delete=models.CASCADE
    )
    taxon = models.ForeignKey(
        Taxon, related_name="fn_catch_counts", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)

    catcnt = models.IntegerField(
        "Total Catch (numbers, including both dead and alive)", blank=True, null=True
    )
    mortcnt = models.IntegerField(
        "Number of dead individuals.", default=0, blank=True, null=True
    )

    comment3 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("effort", "taxon")
        unique_together = ("effort", "taxon")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        self.biocnt = self.fish.count()
        super(FN123NonFish, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}-{}".format(self.effort, self.taxon.itiscode)
