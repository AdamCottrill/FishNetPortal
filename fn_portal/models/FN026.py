from django.db import models
from django.template.defaultfilters import slugify

from .FN011 import FN011


class FN026(models.Model):
    """
    Class to represent the spatial strat used in a project.

    .. note:: We need to revisit how area_lst, site_lst, and sitp_lst work.
       These were original fishnet files. If we keep them, they should be
       changed to fk relationships with associated tables rather than comma
       separated lists
       - clearly and anti-pattern.

    .. note:: we should add a polgyon to this table to capture the spatial
       extent of each spatial strata.  lat-lon are used to provide a centroid -
       may still be required so we can plot spatial strata without polygon
       geoms.

    """

    id = models.AutoField(primary_key=True)

    project = models.ForeignKey(
        "FN011", related_name="spatial_strata", on_delete=models.CASCADE
    )

    label = models.CharField(max_length=110, blank=False, help_text="Space Label")

    space = models.CharField(
        max_length=2, blank=False, help_text="Space Code", db_index=True
    )
    space_des = models.CharField(
        max_length=100, blank=False, help_text="Space Description"
    )
    # this should be fk relationship to another table
    site_lst = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="A list of SITEs that belong to the corresponding spatial stratum",
    )
    # this should be fk relationship to another table
    sitp_lst = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="A list of site types, delimited by comma",
    )
    # this should be fk relationship to another table
    area_lst = models.CharField(
        max_length=100, blank=False, help_text="Space Description"
    )
    grdep_ge = models.FloatField(
        blank=True, null=True, help_text="The lower limit of gear depth (in metres)."
    )

    grdep_lt = models.FloatField(
        blank=True, null=True, help_text="The upper limit of gear depth (in metres)."
    )

    sidep_ge = models.FloatField(
        blank=True,
        null=True,
        help_text="The upper depth limit (in metres) of sites that belong to the corresponding spatial stratum",
    )
    sidep_lt = models.FloatField(
        blank=True,
        null=True,
        help_text="The lower depth limit (in metres) of sites that belong to the corresponding spatial stratum. ",
    )

    grid_ge = models.IntegerField(
        blank=True,
        null=True,
        help_text="The lower limit of grid values belonging to a spatial stratum",
    )
    grid_lt = models.IntegerField(
        blank=True,
        null=True,
        help_text="The upper limit of grid values belonging to a spatial stratum",
    )

    slug = models.SlugField(blank=True, unique=True, editable=False)

    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "FN026 - Spatial Strata"
        verbose_name_plural = "FN026 - Spatial Strata"
        ordering = ["space"]
        unique_together = ["project", "space"]

    def __str__(self):
        """return the object type, the space name, the space code, and
        project code of the project this record is assoicated with.

        """

        repr = "<Space: {} ({}) [{}]>"
        return repr.format(self.space_des, self.space, self.project.prj_cd)

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join([self.project.prj_cd, self.space])

        self.slug = slugify(raw_slug)

        if self.space_des:
            self.label = "{}-{}".format(self.space, self.space_des.title())
        else:
            self.label = "{}".format(self.space)
        super(FN026, self).save(*args, **kwargs)
