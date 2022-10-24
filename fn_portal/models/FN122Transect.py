from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .BaseModel import FNPortalBaseModel
from .FN121 import FN121


class FN122Transecti(FNPortalBaseModel):
    """A table to hold information points associated with gps logs
    that represent transects associated with a sample.  Examples
    include trawls or electrofishing passes.

    """

    id = models.AutoField(primary_key=True)

    sample = models.ForeignKey(
        FN121, related_name="transect_points", on_delete=models.CASCADE
    )
    track_id = models.IntegerField(validators=[MinValueValidator(0)])

    dd_lat = models.FloatField(
        "Latitude (dd)",
        validators=[
            MinValueValidator(41.7),
            MaxValueValidator(49.2),
        ],
    )
    dd_lon = models.FloatField(
        "Longitude (dd)",
        validators=[
            MinValueValidator(-89.6),
            MaxValueValidator(-76.4),
        ],
    )

    sidep = models.FloatField(
        "Site Depth (m)",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(400),
        ],
    )
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

    def clean(self):
        """We can't save an object unless both
        dd_lat and dd_lon are populate or both
        null"""

        if self.dd_lat and self.dd_lon is None:
            msg = "dd_lon cannot be null if dd_lat is provided."
            raise ValidationError(_(msg))
        if self.dd_lat is None and self.dd_lon:
            msg = "dd_lat cannot be null if dd_lon is provided."
            raise ValidationError(_(msg))

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.sample.slug, self.track_id)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        if self.dd_lat and self.dd_lon:
            self.geom = Point(self.dd_lon, self.dd_lat, srid="4326")
        self.full_clean()
        super(FN122Transect, self).save(*args, **kwargs)
