from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F, Sum


from common.models import Lake

User = get_user_model()


class FNProtocol(models.Model):
    """A table to hold information on fishing events/efforts"""

    label = models.CharField(max_length=100, unique=True)
    abbrev = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "{} ({})".format(self.label, self.abbrev)


class FN011(models.Model):
    """Project meta data."""

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
    slug = models.SlugField(max_length=13, unique=True)
    prj_nm = models.CharField(max_length=255)
    # prj_ldr = models.CharField(max_length=255)
    prj_date0 = models.DateField()
    prj_date1 = models.DateField()

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

    def __str__(self):
        return "{} ({})".format(self.gr, self.project.prj_cd)

    def get_projects(self):
        return FN011.objects.filter(samples__gr=self.gr).all()


class FN014(models.Model):
    """FN-II table for Gear Panel Attributes by project-gear"""

    gear = models.ForeignKey(FN013, related_name="gear_effs", on_delete=models.CASCADE)
    eff = models.CharField(max_length=4, blank=True, null=True)
    mesh = models.IntegerField(blank=True, null=True)
    grlen = models.FloatField(blank=True, null=True)
    grht = models.FloatField(blank=True, null=True)
    grwid = models.FloatField(blank=True, null=True)
    grcol = models.CharField(max_length=10, blank=True, null=True)
    grmat = models.CharField(max_length=10, blank=True, null=True)
    gryarn = models.IntegerField(blank=True, null=True)
    grknot = models.IntegerField(blank=True, null=True)
    eff_des = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["eff"]

    def __str__(self):
        return "{}-{} ({})".format(self.gear.gr, self.eff, self.gear.project.prj_cd)
