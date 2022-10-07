from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121


class FN122Transect(FNPortalBaseModel):
    """A table to hold information points associated with gps logs
    that represent transects associated with a sample.  Examples
    include trawls or electrofishing passes.

    """

    id = models.AutoField(primary_key=True)

    sample = models.ForeignKey(
        FN121, related_name="transect_points", on_delete=models.CASCADE
    )
    track_id = models.IntegerField()

    dd_lat = models.FloatField("Latitude (dd)")
    dd_lon = models.FloatField("Longitude (dd)")

    sidep = models.FloatField("Site Depth (m)", blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    timestamp = models.DateTimeField(blank=True, null=True)

    geom = models.PointField(
        "Transect Point",
        srid=4326,
        help_text="Represented as (longitude, latitude)",
        spatial_index=True,
        default=Point(-81, 45),
    )
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ("sample", "track_id")
        unique_together = ("sample", "track_id")

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.sample.slug, self.track_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        if self.dd_lat and self.dd_lon:
            self.geom = Point(self.dd_lon, self.dd_lat, srid="4326")
        super(FN122Transect, self).save(*args, **kwargs)
