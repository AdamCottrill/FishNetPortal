from django.db import models
from django.template.defaultfilters import slugify

from .FN013 import FN013


class FN014(models.Model):
    """
    FN-II table for Gear Panel Attributes by project-gear
    """

    gear = models.ForeignKey(FN013, related_name="gear_effs", on_delete=models.CASCADE)
    eff = models.CharField(max_length=4, blank=True, null=True)
    eff_des = models.TextField(blank=True, null=True)
    mesh = models.IntegerField(blank=True, null=True)
    grlen = models.FloatField(blank=True, null=True)
    grht = models.FloatField(blank=True, null=True)
    grwid = models.FloatField(blank=True, null=True)
    grcol = models.CharField(max_length=10, blank=True, null=True)
    grmat = models.CharField(max_length=10, blank=True, null=True)
    gryarn = models.IntegerField(blank=True, null=True)
    grknot = models.IntegerField(blank=True, null=True)

    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        ordering = ["eff"]

    def __str__(self):
        return "{}-{} ({})".format(self.gear.gr, self.eff, self.gear.project.prj_cd)

    def save(self, *args, **kwargs):
        """"""

        raw_slug = "-".join([self.gear.project.prj_cd, self.gear.gr, self.eff])

        self.slug = slugify(raw_slug)
        super(FN014, self).save(*args, **kwargs)
