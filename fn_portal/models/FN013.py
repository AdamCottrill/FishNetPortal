from django.db import models
from django.template.defaultfilters import slugify

from .FN011 import FN011
from .BaseModel import FNPortalBaseModel


class FN013(FNPortalBaseModel):
    """
    FN-II table for Project Gear
    """

    id = models.AutoField(primary_key=True)

    # sample = models.ForeignKey(FN121, related_name="gear",
    # on_delete=models.CASCADE)
    project = models.ForeignKey(FN011, related_name="gear", on_delete=models.CASCADE)
    gr = models.CharField(max_length=4)
    effcnt = models.IntegerField(blank=True, null=True)
    effdst = models.FloatField(blank=True, null=True)
    gr_des = models.TextField(blank=True, null=True)

    slug = models.SlugField(max_length=20, unique=True)

    def __str__(self):
        return "{} ({})".format(self.gr, self.project.prj_cd)

    def save(self, *args, **kwargs):
        """"""

        raw_slug = "-".join([self.project.prj_cd, self.gr])

        self.slug = slugify(raw_slug)
        super(FN013, self).save(*args, **kwargs)

    def get_projects(self):
        return FN011.objects.filter(samples__gr=self.gr).all()
