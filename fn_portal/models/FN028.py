from django.db import models
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN011 import FN011
from .Gear import Gear


class FN028(FNPortalBaseModel):
    """
    Class to represent the fishing modes used in a project.
    """

    id = models.AutoField(primary_key=True)

    project = models.ForeignKey("FN011", related_name="modes", on_delete=models.CASCADE)
    mode = models.CharField(
        help_text="Mode Code", max_length=2, blank=False, db_index=True
    )
    mode_des = models.CharField(
        help_text="Fishing Mode Description", max_length=100, blank=False
    )
    gear = models.ForeignKey("Gear", related_name="modes", on_delete=models.CASCADE)

    GRUSE_CHOICES = (
        ("1", "Bottom"),
        ("2", "Canned"),
        ("3", "Kyted"),
        ("9", "Unknown"),
    )
    gruse = models.CharField(
        help_text="Code to identify how a gear was used",
        max_length=2,
        blank=False,
        choices=GRUSE_CHOICES,
        default="1",
    )

    ORIENT_CHOICES = [
        ("1", "Perpendicular"),
        ("2", "Paralell"),
        ("3", "Other"),
        ("9", "Unknown"),
        ("U", "Upstream"),
        ("D", "Downstream"),
    ]

    orient = models.CharField(
        help_text="Gear Orientation",
        max_length=2,
        blank=False,
        choices=ORIENT_CHOICES,
        default="9",
    )
    effdur_ge = models.IntegerField(
        blank=True, null=True, help_text="The minimum duration of a fishing effort."
    )
    effdur_lt = models.IntegerField(
        blank=True, null=True, help_text="The maximum duration of a fishing effort."
    )
    efftm0_ge = models.TimeField(
        blank=True,
        null=True,
        help_text="The earliest time of day that fishing effort starts",
    )
    efftm0_lt = models.TimeField(
        blank=True,
        null=True,
        help_text="The latest time of day that fishing effort starts",
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        verbose_name = "FN028 - Fishing Mode"
        ordering = ["mode"]
        unique_together = ["project", "mode"]

    def __str__(self):
        """return the object type, the mode name, the mode code, and
        project code of the project this record is assoicated with.

        """

        repr = "<FishingMode: {} ({}) [{}]>"
        return repr.format(self.mode_des, self.mode, self.project.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized response for this strata.
        If both the mode, and mode_des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.mode_des:
            label = "{}-{}".format(self.mode, self.mode_des.title())
        else:
            label = "{}".format(self.mode)
        return label

    def save(self, *args, **kwargs):
        """Create a unique slug for each fishing mode in this project."""

        raw_slug = "-".join([self.project.prj_cd, self.mode])
        self.slug = slugify(raw_slug)
        super(FN028, self).save(*args, **kwargs)
