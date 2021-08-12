from common.models import Grid5, Species
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import F, Sum
from django.template.defaultfilters import slugify
from django.urls import reverse

from .FN0_tables import FN011, FN022, FN026, FN028

User = get_user_model()


class FN121(models.Model):
    """A table to hold information on fishing events/efforts"""

    project = models.ForeignKey(FN011, related_name="samples", on_delete=models.CASCADE)

    ssn = models.ForeignKey(
        FN022, related_name="samples", blank=True, null=True, on_delete=models.CASCADE
    )
    space = models.ForeignKey(
        FN026, related_name="samples", blank=True, null=True, on_delete=models.CASCADE
    )
    mode = models.ForeignKey(
        FN028, related_name="samples", blank=True, null=True, on_delete=models.CASCADE
    )

    grid5 = models.ForeignKey(
        Grid5,
        related_name="fn_samples",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # move to gear and fn028

    sam = models.CharField(max_length=5, db_index=True)
    effdt0 = models.DateField("Effort Start Date", blank=True, null=True, db_index=True)
    effdt1 = models.DateField("Effort End Date", blank=True, null=True, db_index=True)
    effdur = models.FloatField("Effort Duration (hours)", blank=True, null=True)
    efftm0 = models.TimeField("Effort Start Date", blank=True, null=True, db_index=True)
    efftm1 = models.TimeField("Effort End Time", blank=True, null=True, db_index=True)
    effst = models.CharField(
        "Effort Status", max_length=2, blank=True, null=True, db_index=True
    )

    sitp = models.CharField("Site Type", max_length=4, blank=True, null=True)
    site = models.CharField("Site Label", max_length=100, blank=True, null=True)

    sitem = models.FloatField("Site Temperature (degrees C)", blank=True, null=True)
    sitem0 = models.FloatField(
        "Start Site Temperature (degrees C)", blank=True, null=True
    )
    sitem1 = models.FloatField(
        "End Site Temperature (degrees C)", blank=True, null=True
    )

    sidep = models.FloatField("Site Depth (m)", blank=True, null=True, db_index=True)
    grdepmin = models.FloatField(
        "Min. Gear Depth (m)", blank=True, null=True, db_index=True
    )
    grdepmax = models.FloatField(
        "Max. Gear Depth (m)", blank=True, null=True, db_index=True
    )
    secchi = models.FloatField(blank=True, null=True)
    xslime = models.IntegerField(blank=True, null=True)

    slug = models.SlugField(max_length=100, unique=True)
    dd_lat = models.FloatField("Start Latitude(dd)", blank=True, null=True)
    dd_lon = models.FloatField("Start Longitude (dd)", blank=True, null=True)

    dd_lat1 = models.FloatField("End Latitude (dd)", blank=True, null=True)
    dd_lon1 = models.FloatField("End Longitude (dd)", blank=True, null=True)

    # TODO:
    # geom = models.PointField(srid=4326,
    #                         help_text='Represented as (longitude, latitude)')

    crew = models.CharField(max_length=100, blank=True, null=True)
    comment1 = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ["project", "sam"]
        unique_together = ("project", "sam")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        """When we save a sample, we need to update the associated management
        units, and verify the associated season and space.


        .. todo:: use coordinates to identify associated management unit


        .. todo:: use area_lst and site_lst to verify that space associated with a sample correct.

        """

        if self.effdt0 or self.effdt1:
            sample_date = self.effdt0 if self.effdt0 else self.effdt1
            try:
                self.ssn = self.project.seasons.filter(
                    ssn_date0__lte=sample_date, ssn_date1__gte=sample_date
                ).get()

            except FN022.DoesNotExist:
                msg = "The sample dates for this effort do not fall within a season defined for this project."
                raise ValueError(msg)

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
    """A table to hold information about individual fishing
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
    catwt = models.FloatField("Total Catch Weight (kg)", blank=True, null=True)
    biocnt = models.IntegerField(
        "Number of fish bio-sampled", default=0, blank=True, null=True
    )
    subcnt = models.IntegerField("Number of Fish in Subsample", blank=True, null=True)
    subwt = models.FloatField("Subsample Weight (kg)", blank=True, null=True)

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

    tissue = models.CharField(max_length=20, blank=True, null=True)
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
    food = models.IntegerField("Food Id")
    taxon = models.CharField(
        "A taxonomic code used to identify the type of food item.",
        max_length=10,
        db_index=True,
        blank=True,
        null=True,
    )
    foodcnt = models.IntegerField("Food Count", blank=True, null=True)
    foodval = models.FloatField("Food Measure Value", blank=True, null=True)

    FDMES_CHOICES = (
        (None, "No Data"),
        ("L", "Length"),
        ("W", "Weight"),
        ("V", "Volume"),
    )
    fdmes = models.CharField(
        help_text="Food Measure Code",
        max_length=2,
        blank=True,
        choices=FDMES_CHOICES,
    )

    LIFESTAGE_CHOICES = (
        (None, "No Data"),
        ("10", "10"),
        ("20", "20"),
        ("30", "30"),
        ("40", "40"),
        ("50", "50"),
        ("60", "60"),
    )
    lf = models.CharField(
        help_text="Life Stage",
        max_length=2,
        blank=True,
        choices=LIFESTAGE_CHOICES,
    )

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
    ageid = models.IntegerField("An identifier for an age estimate record")
    agea = models.IntegerField(
        "Age Assessed (yr)", blank=True, null=True, db_index=True
    )
    preferred = models.BooleanField(
        "Preferred age estimate for a fish", default=False, db_index=True
    )
    agest = models.CharField(
        "Age Structure", max_length=5, db_index=True, blank=True, null=True
    )
    xagem = models.CharField("Age Assigned Method", max_length=2, blank=True, null=True)
    agemt = models.CharField("Age Method Data", max_length=5)
    edge = models.CharField("Edge Code", max_length=2, blank=True, null=True)
    conf = models.IntegerField("Confidence", blank=True, null=True)
    nca = models.IntegerField("Number of Complete Annuli", blank=True, null=True)

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
    fish_tag_id = models.IntegerField("Identifier for a Fn125_tag record")
    # tag fields
    tagstat = models.CharField(
        "Tag Status", max_length=5, db_index=True, blank=True, null=True
    )
    tagid = models.CharField(
        "Tag Identification", max_length=20, db_index=True, blank=True, null=True
    )
    tagdoc = models.CharField(
        "Tag Documentation", max_length=6, db_index=True, blank=True, null=True
    )
    xcwtseq = models.CharField(
        "Sequential CWT number", max_length=5, blank=True, null=True
    )
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
