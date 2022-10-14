# from django.db import models
from common.models import Lake, Species
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from .BaseModel import FNPortalBaseModel
from .FN011 import FN011
from .FNProtocol import FNProtocol


class FN012Base(FNPortalBaseModel):
    """The FN012 table functions as a constraint table to ensure that
    catch counts (entries in the FN123 table and lower) are associated
    with a documented species and group. The FN012 also provides a
    mechanism to capture how the catch was processed, sampled, and
    aged, and finally, provides max and min values for several
    attributes of the sampled fish.  This abstract base model is used
    to provide fields that are common the the lake-protocol default
    values as well as the project specific values that may have been
    customized by the project lead.

    """

    id = models.AutoField(primary_key=True)

    slug = models.SlugField(max_length=100, unique=True)
    species = models.ForeignKey(
        Species, related_name="%(class)s_sample_specs", on_delete=models.CASCADE
    )
    grp = models.CharField(max_length=3, default="00", db_index=True)

    grp_des = models.CharField(
        help_text="The meaning of a GRP code or more general information about SPC+GRP.",
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
        ("FLEN", "Fork Length"),
        ("TLEN", "Total Length"),
    )
    sizatt = models.CharField(
        help_text="Size Sample Code",
        max_length=4,
        blank=True,
        null=True,
        default="FLEN",
        choices=SIZATT_CHOICES,
    )

    sizint = models.IntegerField(
        help_text="Size Sample Interval (mm)",
        blank=True,
        null=True,
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
        blank=True,
        null=True,
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

    # from agest entry of data dictionary
    # TODO: move to common lookup table
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
        ("G", "Other (NO LONGER SUPPORTED)"),
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

    agest = models.CharField(max_length=20, default="0")

    AGEDEC2_CHOICES = (
        ("0", "Not validated"),
        ("1", "Validated"),
    )
    agedec2 = models.CharField(
        help_text="Age Method",
        max_length=1,
        blank=True,
        null=True,
        choices=AGEDEC2_CHOICES,
    )

    LAMSAM_CHOICES = (
        ("0", "Not Collected"),
        ("1", "XLAM (NO LONGER SUPPORTED)"),
        ("2", "LAMIJC"),
    )
    lamsam = models.CharField(
        help_text="Lamprey Reporting",
        max_length=1,
        default="2",
        choices=LAMSAM_CHOICES,
    )

    flen_min = models.FloatField(
        "Minimum Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(750)],
    )
    flen_max = models.FloatField(
        "Maximim Fork Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
    )
    tlen_min = models.FloatField(
        "Minimum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(750)],
    )
    tlen_max = models.FloatField(
        "Maximum Total Length (mm)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(2000)],
    )
    rwt_min = models.FloatField(
        "Minimum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.1), MaxValueValidator(55000)],
    )
    rwt_max = models.FloatField(
        "Maximum Round Weight (g)",
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(55000)],
    )
    k_min_error = models.FloatField(
        "Minimum K (TLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.05), MaxValueValidator(5.0)],
    )
    k_min_warn = models.FloatField(
        "Minimum K (TLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.07), MaxValueValidator(4.0)],
    )
    k_max_warn = models.FloatField(
        "Maximum K (FLEN) - warning",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.07), MaxValueValidator(4.0)],
    )

    k_max_error = models.FloatField(
        "Maximum K (FLEN) - error",
        blank=True,
        null=True,
        validators=[MinValueValidator(0.05), MaxValueValidator(5.0)],
    )

    class Meta:
        abstract = True

    def get_slug(self):
        pass

    def save(self, *args, **kwargs):
        slug = self.get_slug()
        if slug:
            self.slug = slugify(slug)
        else:
            pass
        # should we populated default values for size constrains here if none are provided?
        self.full_clean()
        super(FN012Base, self).save(*args, **kwargs)

        return self

    def __str__(self):

        return self.slug

    def clean(self):
        """the agedec, fdsam, and spc mark values are actually composite
        fields. The first value indictates if the data was collected or not,
        the second indicates how. the second should only be populated if the
        first character is something other than 0."""
        if self.agedec1 != "0" and self.agedec2 is None:
            raise ValidationError(_("Invalid AGEDEC code."))
        if (self.fdsam1 == "0" and self.fdsam2 is not None) or (
            self.fdsam1 != "0" and self.fdsam2 is None
        ):
            raise ValidationError(_("Invalid FDSAM code."))
        if (self.spcmrk1 == "0" and self.spcmrk2 is not None) or (
            self.spcmrk1 != "0" and self.spcmrk2 is None
        ):
            raise ValidationError(_("Invalid SPCMRK code."))

    @property
    def fdsam(self):
        """the original fn-II field fdsam is made of two sub fields.  This
        property returns fdsam by concatenating fdsam1 and fdsam2."""

        if self.fdsam1 == "0":
            return self.fdsam1
        else:
            return f"{self.fdsam1}{self.fdsam2}"

    @property
    def spcmrk(self):
        """the original fn-II field spcmrk is made of two sub fields.  This
        property returns spcmrk by concatenating spcmrk1 and spcmrk2."""

        if self.spcmrk1 == "0":
            return self.spcmrk1
        else:
            return f"{self.spcmrk1}{self.spcmrk2}"

    @property
    def agedec(self):
        """the original fn-II field agedec is made of two sub fields.  This
        property returns agedec by concatenating agedec1 and agedec2."""

        if self.agedec2:
            return f"{self.agedec1}{self.agedec2}"
        else:
            return self.agedec1


class FN012(FN012Base):
    """A table to hold the FN012 data for an individual project."""

    project = models.ForeignKey(
        "FN011", related_name="sample_specs", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "FN012 - Project Sampling Specs"
        models.UniqueConstraint(
            fields=["project", "species", "grp"], name="unique_project_species_grp"
        )

    def get_slug(self):
        return f"fn012-{self.project.prj_cd}-{self.species.spc}-{self.grp}"


class FN012Protocol(FN012Base):
    """Default FN012 values for a each lake and protocol."""

    lake = models.ForeignKey(
        Lake, related_name="sample_specs", on_delete=models.CASCADE
    )

    protocol = models.ForeignKey(
        FNProtocol,
        related_name="sample_specs",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "FN012Protocols - Protocol Sampling Specs"
        models.UniqueConstraint(
            fields=["lake", "protocol", "species" "grp"],
            name="unique_lake_protocol_species_grp",
        )
        indexes = [
            models.Index(fields=["lake", "protocol"]),
        ]

    def get_slug(self):
        return (
            f"fn012protocol-{self.lake.abbrev}-{self.protocol.abbrev}"
            + f"-{self.species.spc}-{self.grp}"
        )
