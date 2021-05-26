import factory
import datetime

from common.models import Species, Lake, Grid5
from .user_factory import UserFactory

from ..models import (
    FNProtocol,
    FN011,
    FN121,
    FN122,
    FN123,
    FN125,
    FN126,
    FN127,
    FN125Tag,
    FN125_Lamprey,
    FN013,
    FN014,
    GearFamily,
    Gear,
    SubGear,
    Gear2SubGear,
)


class LakeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lake
        django_get_or_create = ("abbrev",)

    lake_name = "Lake Huron"
    abbrev = "HU"


class Grid5Factory(factory.django.DjangoModelFactory):
    """
    A factory for 5-minute grid objects.
    """

    class Meta:
        model = Grid5
        django_get_or_create = ("lake", "grid")

    grid = 1234
    lake = factory.SubFactory(LakeFactory)

    @factory.lazy_attribute
    def slug(self):
        """
        calculate a slug using lake abbrev and grid number
        """

        return "{}-{:04d}".format(self.lake.abbrev.lower(), self.grid)


class SpeciesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Species
        django_get_or_create = ("spc",)

    spc = factory.Sequence(lambda n: n)
    spc_nmco = "Lake Trout"
    spc_nmsc = "Salvelinus nameychush"


class FNProtocolFactory(factory.django.DjangoModelFactory):
    """A factory for protocl objects."""

    class Meta:
        model = FNProtocol
        django_get_or_create = ("abbrev",)

    label = "Fake Assessment Protocol"
    abbrev = "FAP"


class FN011Factory(factory.django.DjangoModelFactory):
    """A factory for FN011 objects.  Project year, start date and end date
    are all generated after the fact based on project code.
    """

    class Meta:
        model = FN011
        django_get_or_create = ("prj_cd",)

    prj_cd = "LHA_IA18_999"
    prj_nm = "Cool Project"
    prj_ldr = factory.SubFactory(UserFactory)
    lake = factory.SubFactory(LakeFactory)
    protocol = factory.SubFactory(FNProtocolFactory)

    @factory.lazy_attribute
    def prj_date0(self):
        """
        create the start date from the project code
        """
        yr_string = self.prj_cd[6:8]
        year = "19" + yr_string if int(yr_string) > 50 else "20" + yr_string
        datestring = "January 15, {0}".format(year)
        prj_date0 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        return prj_date0

    @factory.lazy_attribute
    def prj_date1(self):
        """
        create the end date from the project code
        """
        yr_string = self.prj_cd[6:8]
        year = "19" + yr_string if int(yr_string) > 50 else "20" + yr_string
        datestring = "January 16, {0}".format(year)
        prj_date1 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        return prj_date1

    @factory.lazy_attribute
    def year(self):
        """
        calculate a based on project code
        """

        yr_string = self.prj_cd[6:8]
        year = "19" + yr_string if int(yr_string) > 50 else "20" + yr_string
        return year


class FN121Factory(factory.django.DjangoModelFactory):
    """A factory for FN121 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN121
        django_get_or_create = ("project", "sam")

    project = factory.SubFactory(FN011Factory)
    sam = factory.Sequence(lambda n: "{:03d}".format(n))


class FN122Factory(factory.django.DjangoModelFactory):
    """A factory for FN122 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN122
        django_get_or_create = ("sample", "eff")

    sample = factory.SubFactory(FN121Factory)
    eff = factory.Sequence(lambda n: "{:03d}".format(n))


class FN123Factory(factory.django.DjangoModelFactory):
    """A factory for FN123 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN123
        django_get_or_create = ("effort", "species", "grp")

    effort = factory.SubFactory(FN122Factory)
    grp = factory.Sequence(lambda n: "{:02d}".format(n))


class FN125Factory(factory.django.DjangoModelFactory):
    """A factory for FN125 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN125
        django_get_or_create = ("catch", "fish")

    catch = factory.SubFactory(FN123Factory)
    fish = factory.Sequence(lambda n: "{:03d}".format(n))


class FN125TagFactory(factory.django.DjangoModelFactory):
    """A factory for FNTag objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN125Tag
        django_get_or_create = ("fish", "fish_tag_id")

    fish = factory.SubFactory(FN125Factory)
    fish_tag_id = factory.Sequence(lambda n: n)
    tagid = factory.Sequence(lambda n: n)
    tagdoc = "25012"
    tagstat = "C"


class FN125LampreyFactory(factory.django.DjangoModelFactory):
    """A factory for FNTag objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN125_Lamprey
        django_get_or_create = ("fish", "lamid")

    fish = factory.SubFactory(FN125Factory)
    lamid = factory.Sequence(lambda n: n)
    lamijc = "A235"
    lamijc_type = "A2"
    lamijc_size = 35


class FN126Factory(factory.django.DjangoModelFactory):
    """A factory for FN126 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN126
        django_get_or_create = ("fish", "food")

    fish = factory.SubFactory(FN125Factory)
    food = factory.Sequence(lambda n: n)
    taxon = "F061"
    foodcnt = 6


class FN127Factory(factory.django.DjangoModelFactory):
    """A factory for FN127 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN127
        django_get_or_create = ("fish", "ageid")

    fish = factory.SubFactory(FN125Factory)
    ageid = factory.Sequence(lambda n: n)
    agea = 6


class FN013Factory(factory.django.DjangoModelFactory):
    """A factory for FN013 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN013
        django_get_or_create = ("project", "gr")

    project = factory.SubFactory(FN011Factory)
    gr = "TP99"


class FN014Factory(factory.django.DjangoModelFactory):
    """A factory for FN014 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN014
        django_get_or_create = ("gear", "eff")

    gear = factory.SubFactory(FN013Factory)
    eff = "00"


class GearFamilyFactory(factory.django.DjangoModelFactory):
    """A factory for GearFamily objects.  Only fields that are required or
    have been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = GearFamily
        django_get_or_create = ("family",)

    family = "Smallfish tall"
    abbrev = "smt"
    gear_type = "GL"


class GearFactory(factory.django.DjangoModelFactory):
    """A factory for Gear objects.  Only fields that are required or
    have been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = Gear
        # django_get_or_create = ("gear",)

    family = factory.SubFactory(GearFamilyFactory)
    gr_label = "Monofilament Gillnet"
    gr_code = "GL10"
    gr_des = "This is a fake gear used for testing."


class SubGearFactory(factory.django.DjangoModelFactory):
    """A factory for SubGear objects.  Only fields that are required or
    have been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = SubGear
        # django_get_or_create = ("gear",)

    family = factory.SubFactory(GearFamilyFactory)
    # gear = factory.SubFactory(GearFactory)
    eff = "051"


class Gear2SubGearFactory(factory.django.DjangoModelFactory):
    """A factory for Gear2SubGear objects.  Only fields that are required or
    have been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = Gear2SubGear
        # django_get_or_create = ("gear",)

    gear = factory.SubFactory(GearFactory)
    subgear = factory.SubFactory(SubGearFactory)
