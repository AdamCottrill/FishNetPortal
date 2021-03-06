from django.contrib.auth import get_user_model
from django.db import models
from markdown import markdown

User = get_user_model()

from .BaseModel import FNPortalBaseModel


class GearFamily(FNPortalBaseModel):
    """
    A model to associate sub-gears with the appropriate gears.  Gears
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

    id = models.AutoField(primary_key=True)

    family = models.CharField(max_length=100)
    abbrev = models.CharField(max_length=10, unique=True)
    gear_type = models.CharField(max_length=2)

    class Meta:
        verbose_name_plural = "Gear Families"

    def __str__(self):
        return "{} ({})".format(self.family, self.abbrev)


class Gear(FNPortalBaseModel):
    """
    A master table of gears.

    This will replaces the FN013 table which descibibed the gears used in each
    project. Each gear will only be defined once and will be associated to each
    Fishing mode by foreign key.

    Gear label is used to display a more meaningful message on gear detail page.

    Custom save method converts the markdown in gr_des to html and populates
    gear type if it is null.

    .. todo:: consider adding constrain to grtp - by convention it has always
       been the first two characters of gear code. Stored as a separate field so
       that an index can be applied to it (it is regularlly used to select
       samples).

    """

    id = models.AutoField(primary_key=True)

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
    gr_label = models.CharField("Gear Label", max_length=100)
    grtp = models.CharField("Gear Type", max_length=2, db_index=True)
    gr_code = models.CharField("Gear Code", max_length=5, db_index=True, unique=True)
    effcnt = models.IntegerField("Effort Count", blank=True, null=True)
    effdst = models.FloatField("Effort Distance(m)", blank=True, null=True)
    gr_des = models.TextField("Gear Description in markdown", blank=True, null=True)
    gr_des_html = models.TextField("Gear Description", blank=True, null=True)
    # has this gear been confirmed - accurate and correct.
    confirmed = models.BooleanField(default=False)
    depreciated = models.BooleanField(default=False)

    def __str__(self):
        return "{} ({})".format(self.gr_label, self.gr_code)

    def save(self, *args, **kwargs):
        if self.grtp is None:
            self.grtp = self.gr_code[:2]
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

    # def get_samcount(self):
    #     return FN121.objects.filter(gr=self.gr_code).count()


class SubGear(FNPortalBaseModel):
    """
    A master table of gear panel attributes.

    Each sub-gear will only be defined once and asscoaited with the
    appropriate gear through a many-to-many relationship.  51mm
    offshore panel is used in multiple gears, and each gear has
    multple panels/subgears.

    NOTE: gear colour, yarn, material and knot should be choice fields
    using Fishnet code tables.

    """

    GRYARN_CHOICES = [(1, "Monofilament"), (2, "Multifilament"), (3, "no data")]

    GRKNOT_CHOICES = [(1, "Knotless"), (2, "Knots present"), (3, "other")]

    GRCOL_CHOICES = [
        ("1", "White"),
        ("2", "Black"),
        ("3", "Green"),
        ("4", "Blue"),
        ("5", "Discoloured White"),
        ("6", "Transparent"),
        ("7", "Other"),
        ("8", "Grey"),
    ]

    GRMAT_CHOICES = [
        ("1", "Polyamide (e.g. Nylon)"),
        ("2", "Polypropylene (e.g. Ulstron)"),
        ("3", "Polyethylene"),
        ("4", "Polyester"),
        ("5", "Cotton"),
        ("6", "Other"),
    ]

    id = models.AutoField(primary_key=True)

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
        return "{}-{}-{}-{} ({})".format(
            self.eff, self.mesh, self.grlen, self.grht, self.family
        )


class Gear2SubGear(FNPortalBaseModel):
    """
    An association table between gears and their sub-gears.

    An explicit association table allows us to use a many-to-many through
    relationship which can include information on panel order
    (defaults to 1 for gear withough sub-efforts or arranged in
    sequential order).

    panel_count is used to adjust the number of subgear panels
    included in some gear codes, particularly multifilament gear that
    were often multiples of 45.72 m (45 m, 91m and in a small number
    of cases 137 m)

    """

    id = models.AutoField(primary_key=True)

    gear = models.ForeignKey(Gear, related_name="gang", on_delete=models.CASCADE)
    subgear = models.ForeignKey(SubGear, related_name="gang", on_delete=models.CASCADE)
    panel_sequence = models.PositiveIntegerField(default=1)
    panel_count = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["panel_sequence", "subgear__eff"]

    def __str__(self):
        return "{} - {}".format(self.gear, self.subgear)


class GearEffortProcessType(FNPortalBaseModel):
    """
    A table to capture the known process types and associated effort for each gear.

    Process type describes how the catch in sample is handled - either
    by net, by mesh size, by groups of panels, or individual panels.
    This table constrains the process types available to each gear to
    those that are known and documented, and ensures that the data
    below the 121 table can be validated.

    1. - By Sample
    -----------

    This process type is for programs that do not split the catch into
    distinct efforts. This is the default process type and is most
    generally associated with trap nets, trawls, and some gill netting
    programs. By convention a default value of '001' is used for EFF
    in these programs.

    One net set, one effort.

    2. - By Mesh Size
    -----------------

    This process type is use for gill net programs that capture catch
    information by mesh size.  This process type is used in most Great
    Lakes Index programs, and FWIN surveys.  By convention, EFF is
    used to capture the mesh size of the panel or panel(s) of each
    effort (e.g. '051' = 51 mm mesh).

    One net set, one effort for each mesh.


    3. - By Panel Group
    -------------------

    This process type captures situations where efforts are identified
    as groups of panels (regardless of their mesh size). The
    prototypical example of this process type is the Spring Littoral
    Index Netting protocol where the gear consist of 6 identical
    panels set perpendicular to shore.  The 3-inshore panel are
    identified as EFF='001' and the three offshore panels are
    identified as EFF='002'.

    one net set -> one effort for each group of panels

    4. - By Panel
    -------------

    This process type is appropriate if the gear has multiple panel of
    the same mesh and the catch in each panel is reported separately.
    This process type is rarely used, but is specified in some
    protocols.  If your gear does not have duplicate panels of the
    same size, or you are not interested in reporting by individual
    panel, Process Type 2 is more appropriate.

    In process type 4, because meshes are repeated, and catch is to be
    reported by panel, the panel mesh size can no longer be used to
    identify the effort (eg = '051' could now refer to more than one
    panel).  As a result panels must be uniquely numbered with values
    that no longer correspond to their mesh size.  Gear descriptions
    and associated efforts must be carefully verified if this process
    type is selected.

    one net set -> one effort per panel

    """

    PROCESS_TYPE_CHOICES = [
        ("1", "By Sample"),
        ("2", "By Mesh Size"),
        ("3", "By Panel Group"),
        ("4", "By Panel"),
        ("5", "Other (TBD)"),
    ]

    id = models.AutoField(primary_key=True)

    gear = models.ForeignKey(
        Gear, related_name="process_types", on_delete=models.CASCADE
    )
    process_type = models.CharField(
        "Process type choice associated with this gear and effort.",
        default="1",
        choices=PROCESS_TYPE_CHOICES,
        max_length=2,
    )
    eff = models.CharField("Effort (EFF) value", default="001", max_length=3)
    effdst = models.FloatField(
        "Effort Distance (m) associated with this gear and effort (optional)",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Gear Process Type"
        ordering = ["gear_id", "process_type", "eff"]
        unique_together = ["gear", "process_type", "eff"]

    def __str__(self):
        return f"{self.gear.gr_code} - {self.process_type} - {self.eff}"
