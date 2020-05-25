from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.db.models import F, Sum

from markdown import markdown

from common.models import Grid5, Lake, Species

User = get_user_model()

# class Species(models.Model):
#     species_code = models.IntegerField(unique=True)
#     common_name = models.CharField(max_length=40, null=True, blank=True)
#     scientific_name = models.CharField(max_length=50, null=True, blank=True)

#     class Meta:
#         ordering = ["common_name"]
#         verbose_name_plural = "Species"

#     def __str__(self):
#         if self.scientific_name:
#             spc_unicode = "{} ({})".format(self.common_name, self.scientific_name)
#         else:
#             spc_unicode = "{}".format(self.common_name)
#         return spc_unicode


class FNProtocol(models.Model):
    """A table to hold information on fishing events/efforts
    """

    label = models.CharField(max_length=100, unique=True)
    abbrev = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return "{} ({})".format(self.label, self.abbrev)


class FN011(models.Model):
    """ Project meta data.
    """

    protocol = models.ForeignKey(
        FNProtocol, related_name="projects", on_delete=models.CASCADE
    )

    prj_ldr = models.ForeignKey(
        User,
        help_text="Project Lead",
        related_name="creels",
        blank=False,
        on_delete=models.CASCADE,
    )
    field_crew = models.ManyToManyField(User)

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


class FN121(models.Model):
    """A table to hold information on fishing events/efforts
    """

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
        # ordering = ['last_name', 'first_name']
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
    """ a table for catch counts.
    """

    effort = models.ForeignKey(FN122, related_name="catch", on_delete=models.CASCADE)
    species = models.ForeignKey(
        Species, related_name="catch_counts", on_delete=models.CASCADE
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
        # ordering = ['last_name', 'first_name']
        unique_together = ("effort", "species", "grp")

    def __str__(self):
        return self.slug.upper()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.fishnet_keys())
        super(FN123, self).save(*args, **kwargs)

    def fishnet_keys(self):
        """return the fish-net II key fields for this record"""
        return "{}-{}-{}".format(self.effort, self.species.spc, self.grp)


class FN125(models.Model):
    """A table for biological data collected from fish
    """

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
        # ordering = ['last_name', 'first_name']
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
    """ a table for diet data collected in the field.
    """

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
    """A table for age interpretations collected from fish
    """

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
    """ a table for lamprey data. """

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
    """ a table for the tag(s) assoicated with a fish.
    """

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


class GearFamily(models.Model):
    """A model to associate sub-gears with the appropriate gears.  Gears
    are comprised of subgears, but only subgears in the same family
    should be allowed.  For example:

    + GL10, GL21, GL22 and GL32 are all derived from offshore
    monofilament (OSIA-mono) panels (and GL18 might be too)

    + GL01 is offshore multifilament (OSIA-multi)

    + GL50 is a fwin family

    + GL38, GL51, GL64 are all part of the FLIN/SLIN family

    + Nordic nets
    + Bottle traps
    + GEE traps
    + Windemere traps

    + Smallfish tall
    + Smallfish short

    + North American Standard (not sure if small and large standards
    are same family or not)

    + TP* is trapnet family
    + HP* is hoopnet family

    + Unknown - this should never be used, but will be included here
    to get things working.  Delete before moving into production.

    Generally, the subgears within a family have similar
    characteristics and are only used in particular gear types. the
    51mm panels in FWIN and offshore gear are different lengths and
    are unlikely to ever be used on the same net.

    """

    family = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=10, unique=True)
    gear_type = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Gear Families"

    def __str__(self):
        return "{} ({})".format(self.family, self.abbrev)


class Gear(models.Model):
    """A master table of gears.  This will evaully replace the FN013
    table.  Each gear will only be defined once and will be associated
    to each SAM by foreign key.
    """

    assigned_to = models.ForeignKey(
        User,
        related_name="assigned_to",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    family = models.ForeignKey(
        GearFamily, related_name="gears", on_delete=models.CASCADE
    )
    gr_label = models.CharField(max_length=100)
    gr_code = models.CharField(max_length=4, db_index=True, unique=True)
    effcnt = models.IntegerField(blank=True, null=True)
    effdst = models.FloatField(blank=True, null=True)
    gr_des = models.TextField(blank=True, null=True)
    gr_des_html = models.TextField(blank=True, null=True)
    # has this gear been confirmed - accurate and correct.
    confirmed = models.BooleanField(default=False)
    depreciated = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.gr_label, self.gr_code)

    def save(self, *args, **kwargs):
        self.gr_des_html = markdown(self.gr_des)
        super(Gear, self).save(*args, **kwargs)

    def get_subgears(self):
        """Return the sub-gears (panels) that make up this gear. in addition
        to the sub gears, get the number of panels of each gear that
        is included in the gang.
        """

        # get the panel counts by subgear
        panel_counts = {}
        for panel in self.gang.values():
            panel_counts[panel["subgear_id"]] = panel["panel_count"]

        # my_subgears = SubGear.objects.filter(gear=self).order_by("gang").all()
        my_subgears = self.subgears.all()
        # now add the panel count attribute to each sub-gear so we can access it
        # templates.
        for subgear_panel in my_subgears:
            subgear_panel.panel_count = panel_counts.get(subgear_panel.id, 0)

        return my_subgears

    def get_samcount(self):
        return FN121.objects.filter(gr=self.gr_code).count()


class SubGear(models.Model):
    """A master table of gear panel attributes - each sub-gear will only
    be defined once and asscoaited with the appropriate gear through a
    many-to-many relationship.  51mm offshore panel is used in
    multiple gears, and each gear has multple panels/subgears.

    NOTE: gear colour, yarn, material and knot should be choice fields
    using Fishnet code tables.

    """

    GRYARN_CHOICES = {(1, "Monofilament"), (2, "Multifilament"), (3, "no data")}

    GRKNOT_CHOICES = {(1, "Knotless"), (2, "Knots present"), (3, "other")}

    GRCOL_CHOICES = {
        ("1", "White"),
        ("2", "Black"),
        ("3", "Green"),
        ("4", "Blue"),
        ("5", "Discoloured White"),
        ("6", "Transparent"),
        ("7", "Other"),
        ("8", "Grey"),
    }

    GRMAT_CHOICES = {
        ("1", "Polyamide (e.g. Nylon)"),
        ("2", "Polypropylene (e.g. Ulstron)"),
        ("3", "Polyethylene"),
        ("4", "Polyester"),
        ("5", "Cotton"),
        ("6", "Other"),
    }

    gear = models.ManyToManyField(
        "Gear", through="Gear2SubGear", related_name="subgears"
    )
    family = models.ForeignKey(
        GearFamily, related_name="subgears", on_delete=models.CASCADE
    )
    eff = models.CharField(max_length=4, blank=True, null=True)
    mesh = models.FloatField(blank=True, null=True)
    grlen = models.FloatField(blank=True, null=True)
    grht = models.FloatField(blank=True, null=True)
    grwid = models.FloatField(blank=True, null=True)
    grcol = models.CharField(
        max_length=10, blank=True, null=True, choices=GRCOL_CHOICES
    )
    grmat = models.CharField(
        max_length=10, blank=True, null=True, choices=GRMAT_CHOICES
    )
    gryarn = models.IntegerField(blank=True, null=True, choices=GRYARN_CHOICES)
    grknot = models.IntegerField(blank=True, null=True, choices=GRKNOT_CHOICES)
    grdiam = models.FloatField(blank=True, null=True)
    tielength = models.FloatField(blank=True, null=True)
    meshes_per_tie = models.PositiveIntegerField(blank=True, null=True)
    meshes_deep = models.PositiveIntegerField(blank=True, null=True)

    eff_des = models.TextField(blank=True, null=True)

    class Meta:
        pass
        # ordering = ['eff',]

    def __str__(self):
        return "{} ({})".format(self.eff, self.family)


class Gear2SubGear(models.Model):
    """An association table between gears and their sub-gears.  An
    explicit association table allows us to use a many-to-many through
    relationship which can include information on panel order
    (defaults to 1 for gear withough sub-efforts or arranged in
    sequential order).

    panel_count is used to adjust the number of subgear panels
    included in some gear codes, particularly multifilament gear that
    were often multiples of 45.72 m (45 m, 91m and in a small number
    of cases 137 m)

    """

    gear = models.ForeignKey(Gear, related_name="gang", on_delete=models.CASCADE)
    subgear = models.ForeignKey(SubGear, related_name="gang", on_delete=models.CASCADE)
    panel_sequence = models.PositiveIntegerField(default=1)
    panel_count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["panel_sequence", "subgear__eff"]

    def __str__(self):
        return "{} - {}".format(self.gear, self.subgear)
