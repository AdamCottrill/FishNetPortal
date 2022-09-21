from django.contrib.gis.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN123 import FN123


class FN125(FNPortalBaseModel):
    """
    A table for biological data collected from fish
    """

    id = models.AutoField(primary_key=True)

    catch = models.ForeignKey(FN123, related_name="fish", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    fish = models.CharField(max_length=6)
    flen = models.IntegerField(blank=True, null=True)
    tlen = models.IntegerField(blank=True, null=True)
    rwt = models.FloatField(blank=True, null=True)
    girth = models.IntegerField(blank=True, null=True)
    clipa = models.CharField(max_length=20, blank=True, null=True)
    clipc = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    mat = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    gon = models.CharField(max_length=4, blank=True, null=True, db_index=True)
    noda = models.CharField(max_length=20, blank=True, null=True)
    nodc = models.CharField(max_length=20, blank=True, null=True)

    tissue = models.CharField(max_length=20, blank=True, null=True)
    agest = models.CharField(max_length=20, blank=True, null=True)
    fate = models.CharField(max_length=2, blank=True, null=True)

    # flags for child tables:
    age_flag = models.BooleanField(default=False)
    stom_flag = models.BooleanField(default=False)
    lam_flag = models.BooleanField(default=False)
    tag_flag = models.BooleanField(default=False)

    comment5 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["catch", "fish"]
        unique_together = ("catch", "fish")

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.catch, self.fish)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125, self).save(*args, **kwargs)
