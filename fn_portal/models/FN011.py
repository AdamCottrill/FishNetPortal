from common.models import Lake
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum
from django.template.defaultfilters import slugify
from django.urls import reverse


User = get_user_model()

from .BaseModel import FNPortalBaseModel
from .Gear import Gear
from .FNProtocol import FNProtocol


class FN011(FNPortalBaseModel):
    """
    Project meta data.

    .. note:: field_crew is currently used in permissions - only dba, project
       lead or field crew members are currently allowed to edit records.  This
       should be refined in the future.

    """

    id = models.AutoField(primary_key=True)

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

    STATUS_CHOICES = (
        ("archive", "Archive"),
        ("initiated", "Initiated"),
        ("validated", "Validated"),
        ("complete", "Complete"),
    )

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="archive")

    class Meta:
        verbose_name_plural = "FN011 - Projects"
        ordering = ["-year", "prj_cd"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.prj_cd)
        if self.year is None or self.year == "":
            yr = self.prj_cd[6:8]
            self.year = f"19{yr}" if int(yr) > 50 else f"20{yr}"
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

        from .FN121 import FN121

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
            FN011.objects.filter(prj_cd=self.prj_cd)
            .values_list("samples__mode__gear__gr_code")
            .distinct()
        )
        if gear_codes:
            return [x[0] for x in gear_codes]
        else:
            return None

    def get_gear(self):
        """Not sure if this is the right way to do this or not or if we even
        need this. - get the list of Gear codes the the 121 table for
        this project. - eventually these should match the gear tables.

        """
        # gear = FN013.objects.filter(project__prj_cd=self.prj_cd).all()
        gear = Gear.objects.filter(modes__project=self).distinct()
        return gear
