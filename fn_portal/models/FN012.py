# from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

from common.models import Species, Lake

from .FN011 import FN011
from .FNProtocol import FNProtocol


class FN012Base(models.Model):
    """
    The FN012 table functions as a contrainted table to ensure that
    catch counts (entries in the FN123 table and lower) are
    documented. It also provides a mechanism to capture how the catch
    was processed, sampled and aged, and finally provides max and min
    values for several attributes of teh sampled fish.  This abstract
    base model is used to provide fields that are common the the
    lake-protocol default values as well as the project specific
    values that may have been customized by the project lead.

    """

    slug = models.SlugField(max_length=100, unique=True)
    species = models.ForeignKey(
        Species, related_name="%(class)s_sample_constraints", on_delete=models.CASCADE
    )
    grp = models.CharField(max_length=3, default="00", db_index=True)

    grp_des = models.CharField(
        "The meaning of a GRP code or more general information about SPC+GRP.",
        max_length=300,
        default="Default Group",
    )

    BIOSAM_CHOICES = (
        ("0", "Not sampled"),
        ("1", "Complete sampling"),
        ("2", "Random sampling"),
        ("3", "Size-stratified sampling"),
    )
    biosam = models.CharField(
        help_text="Biosampling Code",
        max_length=1,
        default="1",
        choices=BIOSAM_CHOICES,
    )

    SIZSAM_CHOICES = (
        ("0", "Not Sampled"),
        ("1", "FN125"),
        ("2", "FN124"),
        ("3", "Both FN124 and FN125"),
    )
    sizsam = models.CharField(
        help_text="Size Sample Code",
        max_length=1,
        default=0,
        choices=SIZSAM_CHOICES,
    )

    SIZATT_CHOICES = (
        ("flen", "Fork Length"),
        ("tlen", "Total Length"),
    )
    sizatt = models.CharField(
        help_text="Size Sample Code",
        max_length=4,
        blank=True,
        null=True,
        default="flen",
        choices=SIZATT_CHOICES,
    )

    sizint = models.IntegerField(
        help_text="Size Sample Interval (mm)",
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(50)],
    )

    # NOTE: - processed/not processed seems like an operational attribute.
    FDSAM1_CHOICES = (
        ("0", "Data not collected"),
        ("1", "Collected, not processed"),
        ("2", "Collected, processed"),
    )

    fdsam1 = models.CharField(
        help_text="FDSAM Sampling Status",
        max_length=1,
        default="0",
        choices=FDSAM1_CHOICES,
    )

    FDSAM2_CHOICES = (
        ("1", "Fish Community and Habitat Section (FCH), Fisheries Branch"),
        ("2", "Haliburton Hastings Fisheries Assessment Unit"),
        ("3", "Other"),
    )

    fdsam2 = models.CharField(
        help_text="FDSAM Taxon Coding Scheme",
        max_length=1,
        default="2",
        choices=FDSAM2_CHOICES,
    )

    SPCMRK1_CHOICES = (
        ("0", "No marks exist & none applied"),
        ("1", "Marks exist & none applied"),
        ("2", "No marks exist & marks applied"),
        ("3", "Marks exist & marks applied"),
    )
    spcmrk1 = models.CharField(
        help_text="Species Mark Exists",
        max_length=1,
        default="0",
        choices=SPCMRK1_CHOICES,
    )

    SPCMRK2_CHOICES = (
        ("0", "Marks not unique marks"),
        ("1", "Marks unique"),
        ("2", "Marks unique and non-unique"),
    )
    spcmrk2 = models.CharField(
        help_text="Species Mark Unique",
        max_length=1,
        blank=True,
        null=True,
        choices=SPCMRK2_CHOICES,
    )

    AGEDEC1_CHOICES = (
        ("0", "No structures sampled"),
        ("1", "Scales (any side)"),
        ("2", "Scales (left side)"),
        ("3", "Scales (right side)"),
        ("4", "Pectoral ray"),
        ("5", "Pectoral spine"),
        ("6", "Pelvic ray"),
        ("7", "Dorsal spine"),
        ("A", "Otolith"),
        ("B", "Operculum"),
        ("C", "Sub-operculum"),
        ("D", "Cleithrum"),
        ("E", "Centrum"),
        ("F", "Branchiostegal"),
        ("G", "Other  (NO LONGER SUPPORTED)"),
        ("M", "Maxilla"),
        ("T", "Tag"),
        ("V", "Vertebrate"),
        ("X", "Methods vary across fish"),
    )

    agedec1 = models.CharField(
        help_text="Age Method",
        max_length=1,
        default="0",
        choices=AGEDEC1_CHOICES,
    )

    AGEDEC2_CHOICES = (
        ("0", "Not validated"),
        ("1", "Validated"),
    )
    agedec2 = models.CharField(
        help_text="Age Method",
        max_length=1,
        default="0",
        choices=AGEDEC2_CHOICES,
    )

    flen_min = models.FloatField(
        "Minimum Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(700)],
    )
    flen_max = models.FloatField(
        "Maximim Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    tlen_min = models.FloatField(
        "Minimum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(700)],
    )
    tlen_max = models.FloatField(
        "Maximum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2000)],
    )
    rwt_min = models.FloatField(
        "Minimum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
    )
    rwt_max = models.FloatField(
        "Maximum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5000)],
    )
    k_min_error = models.FloatField(
        "Minimum K (TLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(2.0)],
    )
    k_min_warn = models.FloatField(
        "Minimum K (TLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(1.5)],
    )
    k_max_error = models.FloatField(
        "Maximum K (FLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(5.0)],
    )
    k_max_warn = models.FloatField(
        "Maximum K (FLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(4.0)],
    )
    flen2tlen_alpha = models.FloatField(
        "Intercept of FLEN-TLEN Regression",
        blank=True,
        null=True,
        validators=[MinValueValidator(-20.0), MaxValueValidator(80.0)],
    )
    flen2tlen_beta = models.FloatField(
        "Slope of FLEN-TLEN Regression",
        blank=True,
        null=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(1.25)],
    )

    class Meta:
        abstract = True

    @property
    def fdsam(self):
        """the original fn-II field fdsam is made of two sub fields.  This
        property returns fdsam by concatenating fdsam1 and fdsam2."""

        return f"{self.fdsam1}{self.fdsam2}"

    @property
    def spcmrk(self):
        """the original fn-II field spcmrk is made of two sub fields.  This
        property returns spcmrk by concatenating spcmrk1 and spcmrk2."""

        return f"{self.spcmrk1}{self.spcmrk2}"

    @property
    def agedec(self):
        """the original fn-II field agedec is made of two sub fields.  This
        property returns agedec by concatenating agedec1 and agedec2."""

        return f"{self.agedec1}{self.agedec2}"


class FN012(FN012Base):
    """A table to hold the FN012 data for an individual project."""

    project = models.ForeignKey(
        "FN011", related_name="sampling_constraints", on_delete=models.CASCADE
    )

    class Meta:
        models.UniqueConstraint(
            fields=["project", "species", "grp"], name="unique_project_species_grp"
        )


class FN012Default(FN012Base):
    """Default FN012 values for a each lake and protocol."""

    lake = models.ForeignKey(
        Lake, related_name="default_sampling_constraints", on_delete=models.CASCADE
    )

    protocol = models.ForeignKey(
        FNProtocol,
        related_name="default_sampling_constraints",
        on_delete=models.CASCADE,
    )

    class Meta:
        models.UniqueConstraint(
            fields=["lake", "protocol", "species" "grp"],
            name="unique_lake_protocol_species_grp",
        )
