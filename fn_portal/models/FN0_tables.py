from common.models import Lake
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum
from django.template.defaultfilters import slugify
from django.urls import reverse

User = get_user_model()

from .Gear import Gear


class FNProtocol(models.Model):
    """A table to hold information on fishing events/efforts"""

    label = models.CharField(max_length=100, unique=True)
    abbrev = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "{} ({})".format(self.label, self.abbrev)


class FN011(models.Model):
    """Project meta data.

    .. note:: field_crew is currently used in permissions - only dba, project
       lead or field crew members are currently allowed to edit records.  This
       should be refined in the future.

    """

    protocol = models.ForeignKey(
        FNProtocol, related_name="projects", on_delete=models.CASCADE
    )

    prj_ldr = models.ForeignKey(
        User,
        help_text="Project Lead",
        related_name="fn_projects",
        blank=False,
        on_delete=models.CASCADE,
    )

    field_crew = models.ManyToManyField(User, related_name="fn_field_crew")

    year = models.CharField(max_length=4, db_index=True)
    prj_cd = models.CharField(max_length=13, db_index=True, unique=True)
    prj_nm = models.CharField(max_length=255)
    prj_date0 = models.DateField()
    prj_date1 = models.DateField()

    slug = models.SlugField(max_length=13, unique=True)

    lake = models.ForeignKey(Lake, related_name="projects", on_delete=models.CASCADE)

    SOURCE_CHOICES = (
        ("offshore", "Offshore Index"),
        ("nearshore", "Nearshore Index"),
        ("smallfish", "Smallfish Program"),
    )

    source = models.CharField(
        max_length=255, choices=SOURCE_CHOICES, default="offshore"
    )

    comment0 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-year", "-prj_date1"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.prj_cd)
        super(FN011, self).save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.prj_nm, self.prj_cd)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}".format(self.prj_cd)

    def get_absolute_url(self):
        return reverse("fn_portal:project_detail", args=[str(self.slug)])

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

        from .FN1_tables import FN121

        catcnts = (
            FN121.objects.filter(project=self)
            .annotate(species=F("effort__catch__species__spc_nmco"))
            .annotate(spc=F("effort__catch__species__spc"))
            .values("species", "spc")
            .annotate(catcnts=Sum("effort__catch__catcnt"))
            .annotate(biocnts=Sum("effort__catch__biocnt"))
            .exclude(catcnts__isnull=True)
            .order_by("species")
        )

        return catcnts

    def get_121_gear_codes(self):
        """Not sure if this is the right way to do this or not or if we even
        need this. - get the list of Gear codes the the 121 table for
        this project. - eventually these should match the gear tables.

        returns None or a list of gear codes (e.g. ['GL10', 'GL21'])

        """
        gear_codes = (
            FN011.objects.filter(prj_cd=self.prj_cd).values("samples__gr").distinct()
        )
        if gear_codes:
            return [x.get("samples__gr") for x in gear_codes]
        else:
            return None

    def get_gear(self):
        """Not sure if this is the right way to do this or not or if we even
        need this. - get the list of Gear codes the the 121 table for
        this project. - eventually these should match the gear tables.

        """
        gear = FN013.objects.filter(project__prj_cd=self.prj_cd).all()
        return gear


class FN013(models.Model):
    """FN-II table for Project Gear"""

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


class FN014(models.Model):
    """FN-II table for Gear Panel Attributes by project-gear"""

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


class FN022(models.Model):
    """Class to represent the seasons (temporal strata) used in each project.

    .. todo:: Add range constraints to ssn_date0 and ssn_date1 - they cannot
    overlap each other and must be contained within the project start and end
    dates (project.prj_date0 and project.prj_date1).

    """

    project = models.ForeignKey(
        "FN011", related_name="seasons", on_delete=models.CASCADE
    )
    ssn = models.CharField(
        help_text="Season Code", max_length=2, blank=False, db_index=True
    )
    ssn_des = models.CharField(
        help_text="Season Description", max_length=60, blank=False
    )
    ssn_date0 = models.DateField(help_text="Season Start Date", blank=False)
    ssn_date1 = models.DateField(help_text="Season End Date", blank=False)

    slug = models.SlugField(blank=True, unique=True, editable=False)

    class Meta:
        verbose_name = "FN022 - Season"
        ordering = ["ssn"]
        unique_together = ["project", "ssn"]

    def save(self, *args, **kwargs):
        """"""

        raw_slug = "-".join([self.project.prj_cd, self.ssn])

        self.slug = slugify(raw_slug)
        super(FN022, self).save(*args, **kwargs)

    def __str__(self):
        """return the season name, code and project code associated with this
        particular season."""

        repr = "<Season: {} ({}) [{}]>"
        return repr.format(self.ssn_des, self.ssn, self.project.prj_cd)

    @property
    def label(self):
        """a string that will be used in serialized respoonse for this strata.
        If both the ssn, and ssn des are available, return them, otherwise,
        return just the snn code.

        Arguments:
        - `self`:

        """
        if self.ssn_des:
            label = "{}-{}".format(self.ssn, self.ssn_des.title())
        else:
            label = "{}".format(self.ssn)
        return label


class FN026(models.Model):
    """Class to represent the spatial strat used in a project.

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

    ddlat = models.FloatField(blank=True, null=True)
    ddlon = models.FloatField(blank=True, null=True)

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


class FN028(models.Model):
    """Class to represent the fishing modes used in a project."""

    project = models.ForeignKey("FN011", related_name="modes", on_delete=models.CASCADE)
    mode = models.CharField(
        help_text="Mode Code", max_length=2, blank=False, db_index=True
    )
    mode_des = models.CharField(
        help_text="Fishing Mode Description", max_length=100, blank=False
    )
    gr = models.ForeignKey("Gear", related_name="modes", on_delete=models.CASCADE)

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
