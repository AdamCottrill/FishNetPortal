from common.models import Grid5, ManagementUnit
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.db.models import F, Sum
from django.urls import reverse
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from . import FN011, FN022, FN026, FN026Subspace, FN028


class FN121(FNPortalBaseModel):
    """
    A table to hold information on fishing events/efforts
    """

    id = models.AutoField(primary_key=True)

    management_units = models.ManyToManyField(
        ManagementUnit, related_name="fn121_samples", blank=True
    )

    project = models.ForeignKey(FN011, related_name="samples", on_delete=models.CASCADE)

    ssn = models.ForeignKey(
        FN022, related_name="samples", blank=True, null=True, on_delete=models.CASCADE
    )

    subspace = models.ForeignKey(
        FN026Subspace,
        related_name="samples",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    mode = models.ForeignKey(
        FN028, related_name="samples", blank=True, null=True, on_delete=models.CASCADE
    )

    grid5 = models.ForeignKey(
        Grid5,
        related_name="fn_samples",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # move to gear and fn028

    sam = models.CharField(max_length=5, db_index=True)
    effdt0 = models.DateField("Effort Start Date", blank=True, null=True, db_index=True)
    effdt1 = models.DateField("Effort End Date", blank=True, null=True, db_index=True)
    effdur = models.FloatField("Effort Duration (hours)", blank=True, null=True)
    efftm0 = models.TimeField("Effort Start Date", blank=True, null=True, db_index=True)
    efftm1 = models.TimeField("Effort End Time", blank=True, null=True, db_index=True)
    effst = models.CharField(
        "Effort Status", max_length=2, blank=True, null=True, db_index=True
    )

    sitp = models.CharField("Site Type", max_length=4, blank=True, null=True)
    site = models.CharField("Site Label", max_length=100, blank=True, null=True)

    sitem = models.FloatField("Site Temperature (degrees C)", blank=True, null=True)
    sitem0 = models.FloatField(
        "Start Site Temperature (degrees C)", blank=True, null=True
    )
    sitem1 = models.FloatField(
        "End Site Temperature (degrees C)", blank=True, null=True
    )

    sidep0 = models.FloatField("Site Depth 0 (m)", blank=True, null=True, db_index=True)
    sidep1 = models.FloatField("Site Depth 1 (m)", blank=True, null=True, db_index=True)

    grdepmin = models.FloatField(
        "Min. Gear Depth (m)", blank=True, null=True, db_index=True
    )
    grdepmax = models.FloatField(
        "Max. Gear Depth (m)", blank=True, null=True, db_index=True
    )
    secchi0 = models.FloatField("First Secchi Depth", blank=True, null=True)

    slime = models.IntegerField(blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)
    dd_lat0 = models.FloatField("Start Latitude(dd)", blank=True, null=True)
    dd_lon0 = models.FloatField("Start Longitude (dd)", blank=True, null=True)

    dd_lat1 = models.FloatField("End Latitude (dd)", blank=True, null=True)
    dd_lon1 = models.FloatField("End Longitude (dd)", blank=True, null=True)

    geom = models.PointField(
        "Sample Point",
        srid=4326,
        help_text="Represented as (longitude, latitude)",
        spatial_index=True,
        default=Point(-81, 45),
    )

    crew = models.CharField(max_length=100, blank=True, null=True)
    comment1 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["project", "sam"]
        unique_together = ("project", "sam")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        """When we save a sample, we need to update the associated management
        units, and verify the associated season and space.


        .. todo:: use coordinates to identify associated management unit


        .. todo:: use area_lst and site_lst to verify that space associated with a sample correct.

        """

        if self.effdt0 or self.effdt1:
            sample_date = self.effdt0 if self.effdt0 else self.effdt1
            try:
                self.ssn = self.project.seasons.filter(
                    ssn_date0__lte=sample_date, ssn_date1__gte=sample_date
                ).get()

            except FN022.DoesNotExist:
                msg = "The sample dates for this effort do not fall within a season defined for this project."
                raise ValueError(msg)

        if self.dd_lat0 and self.dd_lon0:
            self.geom = Point(self.dd_lon0, self.dd_lat0, srid="4326")

        self.slug = slugify(self.fishnet_keys())

        super(FN121, self).save(*args, **kwargs)

        if self.geom:
            mus = ManagementUnit.objects.filter(geom__contains=self.geom)
            self.management_units.set(mus)
        return self

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.project.prj_cd, self.sam)

    def get_absolute_url(self):
        return reverse(
            "fn_portal:sample_detail", args=[str(self.project.slug), str(self.sam)]
        )

    def total_catch(self):
        """

        Arguments:
        - `self`:
        """

        catch_counts = self.catch_counts()

        return {
            "total": sum([x["catcnts"] for x in catch_counts]),
            "spc_cnt": len(catch_counts),
        }

    def catch_counts(self):
        """

        Arguments:
        - `self`:
        """

        from .FN122 import FN122

        catcnts = (
            FN122.objects.filter(sample=self, catch__catcnt__isnull=False)
            .annotate(
                species=F("catch__species__spc_nmco"), spc=F("catch__species__spc")
            )
            .values("species", "spc")
            .annotate(biocnts=Sum("catch__biocnt"), catcnts=Sum("catch__catcnt"))
            .order_by("species")
        )

        return catcnts
