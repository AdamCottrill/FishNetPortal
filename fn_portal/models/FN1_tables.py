from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F, Sum

from common.models import Grid5, Species

from .FN0_tables import FN011

User = get_user_model()


class FN121(models.Model):
    """A table to hold information on fishing events/efforts"""

    project = models.ForeignKey(FN011, related_name="samples", on_delete=models.CASCADE)

    grid = models.ForeignKey(
        Grid5,
        related_name="fn_samples",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    grtp = models.CharField(max_length=3, blank=True, null=True, db_index=True)
    gr = models.CharField(max_length=5, db_index=True, blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)
    sam = models.CharField(max_length=5, db_index=True)
    effdt0 = models.DateField(blank=True, null=True, db_index=True)
    effdt1 = models.DateField(blank=True, null=True, db_index=True)
    effdur = models.FloatField(blank=True, null=True)
    efftm0 = models.TimeField(blank=True, null=True, db_index=True)
    efftm1 = models.TimeField(blank=True, null=True, db_index=True)
    effst = models.CharField(max_length=2, blank=True, null=True, db_index=True)

    orient = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    sidep = models.FloatField(default=0, blank=True, null=True, db_index=True)
    secchi = models.FloatField(blank=True, null=True)

    site = models.CharField(max_length=100, blank=True, null=True)
    sitem = models.CharField(max_length=5, blank=True, null=True)
    dd_lat = models.FloatField(blank=True, null=True)
    dd_lon = models.FloatField(blank=True, null=True)
    # TODO:
    # geom = models.PointField(srid=4326,
    #                         help_text='Represented as (longitude, latitude)')

    comment1 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["project", "sam"]
        unique_together = ("project", "sam")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN121, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.project.prj_cd, self.sam)

    def get_absolute_url(self):
        return reverse(
            "fn_portal:sample_detail", args=[str(self.project.slug), str(self.sam)]
        )

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

        catcnts = (
            FN122.objects.filter(sample=self)
            .annotate(species=F("catch__species__spc_nmco"))
            .annotate(spc=F("catch__species__spc"))
            .values("species", "spc")
            .annotate(catcnts=Sum("catch__catcnt"))
            .annotate(biocnts=Sum("catch__biocnt"))
            .exclude(catcnts__isnull=True)
            .order_by("species")
        )

        return catcnts


class FN122(models.Model):
    """A table to hold inforamtion about indivual fishing
    efforts(mesh/panel attributes)

    """

    sample = models.ForeignKey(FN121, related_name="effort", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    # sam = models.CharField(max_length=5, blank=True, null=True)
    eff = models.CharField(max_length=4, db_index=True, default=1)
    effdst = models.FloatField(blank=True, null=True)
    grdep = models.FloatField(blank=True, null=True)
    grtem0 = models.FloatField(blank=True, null=True)
    grtem1 = models.FloatField(blank=True, null=True)
    waterhaul = models.BooleanField(default=False)
    comment2 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("sample", "eff")
        unique_together = ("sample", "eff")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN122, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.sample, self.eff)


class FN123(models.Model):
    """a table for catch counts."""

    effort = models.ForeignKey(FN122, related_name="catch", on_delete=models.CASCADE)
    species = models.ForeignKey(
        Species, related_name="fn_catch_counts", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    grp = models.CharField(max_length=3, default="00", db_index=True)
    catcnt = models.IntegerField("Total Catch (numbers)", blank=True, null=True)
    count_only = models.IntegerField(
        "Fish counted but not sampled", blank=True, null=True
    )
    catwt = models.FloatField("Total Catch Weight", blank=True, null=True)
    biocnt = models.IntegerField(
        "Number of fish bio-sampled", default=0, blank=True, null=True
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("effort", "species", "grp")
        unique_together = ("effort", "species", "grp")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN123, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}-{}".format(self.effort, self.species.spc, self.grp)


class FN124(models.Model):
    """a table for catch tallies."""

    catch = models.ForeignKey(
        FN123, related_name="length_tallies", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    siz = models.PositiveIntegerField()
    sizcnt = models.PositiveIntegerField()

    class Meta:
        ordering = ["catch", "siz"]
        unique_together = ("catch", "siz")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN124, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.catch, self.siz)


class FN125(models.Model):
    """A table for biological data collected from fish"""

    catch = models.ForeignKey(FN123, related_name="fish", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    fish = models.CharField(max_length=6)
    flen = models.IntegerField(blank=True, null=True)
    tlen = models.IntegerField(blank=True, null=True)
    rwt = models.IntegerField(blank=True, null=True)
    girth = models.IntegerField(blank=True, null=True)
    clipa = models.CharField(max_length=20, blank=True, null=True)
    clipc = models.CharField(max_length=20, blank=True, null=True)
    sex = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    mat = models.CharField(max_length=2, blank=True, null=True, db_index=True)
    gon = models.CharField(max_length=4, blank=True, null=True, db_index=True)
    noda = models.CharField(max_length=20, blank=True, null=True)
    nodc = models.CharField(max_length=20, blank=True, null=True)
    agest = models.CharField(max_length=20, blank=True, null=True)
    fate = models.CharField(max_length=2, blank=True, null=True)

    # flags for child tables:
    age_flag = models.BooleanField(default=False)
    stom_flag = models.BooleanField(default=False)
    lam_flag = models.BooleanField(default=False)
    tag_flag = models.BooleanField(default=False)

    comment5 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["catch", "fish"]
        unique_together = ("catch", "fish")

    def __str__(self):
        return self.slug.upper()

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.catch, self.fish)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125, self).save(*args, **kwargs)


class FN126(models.Model):
    """a table for diet data collected in the field."""

    fish = models.ForeignKey(FN125, related_name="diet_data", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    food = models.IntegerField()

    taxon = models.CharField(max_length=10, db_index=True, blank=True, null=True)
    foodcnt = models.IntegerField(blank=True, null=True)
    comment6 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "food"]
        unique_together = ("fish", "food")

    def __str__(self):
        return "{} ({}: {})".format(self.slug.upper(), self.taxon, self.foodcnt)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN126, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.food)


class FN127(models.Model):
    """A table for age interpretations collected from fish"""

    fish = models.ForeignKey(
        FN125, related_name="age_estimates", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    ageid = models.IntegerField()
    agea = models.IntegerField(blank=True, null=True, db_index=True)
    preferred = models.BooleanField(default=False, db_index=True)
    agest = models.CharField(max_length=5, db_index=True, blank=True, null=True)
    xagem = models.CharField(max_length=2, blank=True, null=True)
    agemt = models.CharField(max_length=5)
    edge = models.CharField(max_length=2, blank=True, null=True)
    conf = models.IntegerField(blank=True, null=True)
    nca = models.IntegerField(blank=True, null=True)

    ageaDate = models.DateTimeField(blank=True, null=True)

    comment7 = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "ageid"]
        unique_together = ("fish", "ageid")

    def __str__(self):
        return "{} (age={})".format(self.slug.upper(), self.agea)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN127, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.ageid)


class FN125_Lamprey(models.Model):
    """a table for lamprey data."""

    fish = models.ForeignKey(
        FN125, related_name="lamprey_marks", on_delete=models.CASCADE
    )
    slug = models.SlugField(max_length=100, unique=True)
    lamid = models.IntegerField()
    xlam = models.CharField(max_length=6, blank=True, null=True)
    lamijc = models.CharField(max_length=50, blank=True, null=True)

    LAMIJC_TYPE_CHOICES = (
        ["0", "0"],
        ["a1", "A1"],
        ["a2", "A2"],
        ["a3", "A3"],
        ["a4", "A4"],
        ["b1", "B1"],
        ["b2", "B2"],
        ["b3", "B3"],
        ["b4", "B4"],
    )
    lamijc_type = models.CharField(
        max_length=2, choices=LAMIJC_TYPE_CHOICES, default="0"
    )

    lamijc_size = models.IntegerField(blank=True, null=True)
    comment_lam = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["slug", "lamid"]

    # unique_together = ('fish', 'tagnum', 'grp')

    def __str__(self):

        if self.xlam:
            return "{} (xlam: {})".format(self.slug.upper(), self.xlam)
        else:
            return "{} (lamijc: {})".format(self.slug.upper(), self.lamijc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125_Lamprey, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.lamid)


# NOTE - this should be named FN125_Tag
class FN125Tag(models.Model):
    """a table for the tag(s) assoicated with a fish."""

    fish = models.ForeignKey(FN125, related_name="fishtags", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)
    fish_tag_id = models.IntegerField()
    # tag fields
    tagstat = models.CharField(max_length=5, db_index=True, blank=True, null=True)
    tagid = models.CharField(max_length=20, db_index=True, blank=True, null=True)
    tagdoc = models.CharField(max_length=6, db_index=True, blank=True, null=True)
    xcwtseq = models.CharField(max_length=5, blank=True, null=True)
    xtaginckd = models.CharField(max_length=6, blank=True, null=True)
    xtag_chk = models.CharField(max_length=50, blank=True, null=True)

    comment_tag = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["fish", "fish_tag_id"]
        unique_together = ("fish", "fish_tag_id")

    def __str__(self):
        return "{} ({} ({}))".format(self.slug.upper(), self.tagid, self.tagdoc)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN125Tag, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}".format(self.fish, self.fish_tag_id)
