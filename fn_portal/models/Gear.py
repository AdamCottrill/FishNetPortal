from django.contrib.auth import get_user_model
from django.db import models

from markdown import markdown

from .FN1_tables import FN121

User = get_user_model()


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
