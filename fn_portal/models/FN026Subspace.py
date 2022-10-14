from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import IntegrityError, models
from django.db.models import UniqueConstraint
from django.utils.text import slugify

from .BaseModel import FNPortalBaseModel
from .FN026 import FN026


class FN026Subspace(FNPortalBaseModel):
    """
    Class to represent the spatial sub strata used in a project.

    .. note:: we should add a polgyon to this table to capture the spatial
       extent of each spatial strata.  lat-lon are used to provide a centroid -
       may still be required so we can plot spatial strata without polygon
       geoms.

    """

    id = models.AutoField(primary_key=True)

    space = models.ForeignKey(
        FN026, related_name="spatial_substrata", on_delete=models.CASCADE
    )

    subspace = models.CharField(
        max_length=4, blank=False, help_text="Subspace Code", db_index=True
    )
    subspace_des = models.CharField(
        max_length=100, blank=False, help_text="Subspace Description"
    )
    # this should be fk relationship to another table
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

    subspace_wt = models.FloatField(
        blank=True,
        null=True,
        help_text="A weighting factor assigned to a SUBSPACE",
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    slug = models.SlugField(blank=True, unique=True, editable=False)

    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "FN026Subspace - Spatial Substrata"
        verbose_name_plural = "FN026Subspace - Spatial Substrata"
        ordering = ["subspace"]
        constraints = [
            UniqueConstraint(
                fields=["space", "subspace"],
                name="unique_subspace_code",
            ),
            UniqueConstraint(
                fields=["space", "subspace_des"],
                name="unique_subspace_des",
            ),
        ]

    def __str__(self):
        """return the object type, the space name, the space code, and
        project code of the project this record is assoicated with.

        """

        repr = "<Subspace: {} ({}-{}) [{}]>"
        return repr.format(
            self.subspace_des,
            self.space.space,
            self.subspace,
            self.space.project.prj_cd,
        )

    @property
    def label(self):
        """"""
        if self.subspace_des:
            return "{}-{}".format(self.subspace, self.subspace_des.title())
        else:
            return self.subspace

    def clean(self):

        values = (
            FN026Subspace.objects.filter(space=self.space)
            .exclude(pk=self.pk)
            .values_list("subspace", "subspace_des")
        )

        subspaces = [x[0].upper() for x in values]
        subspace_des = [x[1].upper() for x in values]

        sspace = "" if not self.subspace else self.subspace
        sspace_des = "" if not self.subspace_des else self.subspace_des
        if sspace.upper() in subspaces or sspace_des.upper() in subspace_des:
            errmsg = "subspace or subspace_des values already exist in this space"
            raise IntegrityError(errmsg)

        # check that the subspace and subspace_desc are not already used in this project.
        values = (
            FN026Subspace.objects.filter(space__project=self.space.project)
            .exclude(pk=self.pk)
            .values_list("subspace", "subspace_des")
        )

        subspaces = [x[0].upper() for x in values]
        subspace_des = [x[1].upper() for x in values]

        sspace = "" if not self.subspace else self.subspace
        sspace_des = "" if not self.subspace_des else self.subspace_des
        if sspace.upper() in subspaces or sspace_des.upper() in subspace_des:
            errmsg = "subspace or subspace_des values already exist in this project"
            raise IntegrityError(errmsg)

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join(
            [self.space.project.prj_cd, self.space.space, self.subspace]
        )

        self.slug = slugify(raw_slug)
        self.clean()
        super(FN026Subspace, self).save(*args, **kwargs)


from .BaseModel import FNPortalBaseModel
from .FN026 import FN026


class FN026Subspace(FNPortalBaseModel):
    """
    Class to represent the spatial sub strata used in a project.

    .. note:: we should add a polgyon to this table to capture the spatial
       extent of each spatial strata.  lat-lon are used to provide a centroid -
       may still be required so we can plot spatial strata without polygon
       geoms.

    """

    id = models.AutoField(primary_key=True)

    space = models.ForeignKey(
        FN026, related_name="spatial_substrata", on_delete=models.CASCADE
    )

    subspace = models.CharField(
        max_length=4, blank=False, help_text="Subspace Code", db_index=True
    )
    subspace_des = models.CharField(
        max_length=100, blank=False, help_text="Subspace Description"
    )
    # this should be fk relationship to another table
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

    subspace_wt = models.FloatField(
        blank=True,
        null=True,
        help_text="A weighting factor assigned to a SUBSPACE",
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )
    slug = models.SlugField(blank=True, unique=True, editable=False)

    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)

    class Meta:
        verbose_name = "FN026Subspace - Spatial Substrata"
        verbose_name_plural = "FN026Subspace - Spatial Substrata"
        ordering = ["subspace"]
        constraints = [
            UniqueConstraint(
                fields=["space", "subspace"],
                name="unique_subspace_code",
            ),
            UniqueConstraint(
                fields=["space", "subspace_des"],
                name="unique_subspace_des",
            ),
        ]

    def __str__(self):
        """return the object type, the space name, the space code, and
        project code of the project this record is assoicated with.

        """

        repr = "<Subspace: {} ({}-{}) [{}]>"
        return repr.format(
            self.subspace_des,
            self.space.space,
            self.subspace,
            self.space.project.prj_cd,
        )

    @property
    def label(self):
        """"""
        if self.subspace_des:
            return "{}-{}".format(self.subspace, self.subspace_des.title())
        else:
            return self.subspace

    def clean(self):

        values = (
            FN026Subspace.objects.filter(space=self.space)
            .exclude(pk=self.pk)
            .values_list("subspace", "subspace_des")
        )

        subspaces = [x[0].upper() for x in values]
        subspace_des = [x[1].upper() for x in values]

        sspace = "" if not self.subspace else self.subspace
        sspace_des = "" if not self.subspace_des else self.subspace_des
        if sspace.upper() in subspaces or sspace_des.upper() in subspace_des:
            errmsg = "subspace or subspace_des values already exist in this space"
            raise IntegrityError(errmsg)

        # check that the subspace and subspace_desc are not already used in this project.
        values = (
            FN026Subspace.objects.filter(space__project=self.space.project)
            .exclude(pk=self.pk)
            .values_list("subspace", "subspace_des")
        )

        subspaces = [x[0].upper() for x in values]
        subspace_des = [x[1].upper() for x in values]

        sspace = "" if not self.subspace else self.subspace
        sspace_des = "" if not self.subspace_des else self.subspace_des
        if sspace.upper() in subspaces or sspace_des.upper() in subspace_des:
            errmsg = "subspace or subspace_des values already exist in this project"
            raise IntegrityError(errmsg)

    def save(self, *args, **kwargs):
        """
        Create a space label as a combination of the space description
        and space code.
        """

        raw_slug = "-".join(
            [self.space.project.prj_cd, self.space.space, self.subspace]
        )

        self.slug = slugify(raw_slug)
        self.clean()
        super(FN026Subspace, self).save(*args, **kwargs)
