import datetime

import factory

from ...models import (
    FN011,
    FN012,
    FN012Protocol,
    FN013,
    FN014,
    FN022,
    FN026,
    FN028,
    FNProtocol,
    ProjectGearProcessType,
)
from .common_factories import LakeFactory, SpeciesFactory
from .gear_factories import GearFactory
from .user_factory import UserFactory


class FNProtocolFactory(factory.django.DjangoModelFactory):
    """A factory for protocl objects."""

    class Meta:
        model = FNProtocol
        django_get_or_create = ("abbrev",)

    label = factory.Sequence(
        lambda n: "Fake Assessment Protocol - {:02d}".format(n)[-2:]
    )
    abbrev = "FAP"
    description = "This is a fake protocol used for testing."
    active = True
    confirmed = True


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
        Create the start date from the project code - January 1 by default.
        """
        yr_string = self.prj_cd[6:8]
        year = "19" + yr_string if int(yr_string) > 50 else "20" + yr_string
        datestring = "January 1, {0}".format(year)
        prj_date0 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        return prj_date0

    @factory.lazy_attribute
    def prj_date1(self):
        """
        create the end date from the project code - use December 31 by default.
        """
        yr_string = self.prj_cd[6:8]
        year = "19" + yr_string if int(yr_string) > 50 else "20" + yr_string
        datestring = "December 30, {0}".format(year)
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


class ProjectGearProcessTypeFactory(factory.django.DjangoModelFactory):
    """A factory for FN013 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = ProjectGearProcessType
        django_get_or_create = ("project", "gear", "process_type")

    project = factory.SubFactory(FN011Factory)
    gear = factory.SubFactory(GearFactory)
    process_type = 1


class FN012Factory(factory.django.DjangoModelFactory):
    """A factory for FN012 objects."""

    class Meta:
        model = FN012
        django_get_or_create = ("project", "species", "grp")

    project = factory.SubFactory(FN011Factory)
    species = factory.SubFactory(SpeciesFactory)
    grp = "00"
    grp_des = "default group"
    biosam = "1"
    sizsam = 1
    sizatt = "FLEN"
    sizint = 1
    fdsam1 = "0"
    spcmrk1 = "0"
    agedec1 = "X"
    agedec2 = "0"
    flen_min = 150
    flen_max = 750
    tlen_min = 150
    tlen_max = 750
    rwt_min = 100
    rwt_max = 2500
    k_min_error = 0.2
    k_min_warn = 0.5
    k_max_error = 3.5
    k_max_warn = 3.0


class FN012ProtocolFactory(factory.django.DjangoModelFactory):
    """A factory for FN012Protocol objects."""

    class Meta:
        model = FN012Protocol
        django_get_or_create = ("protocol", "lake", "species", "grp")

    protocol = factory.SubFactory(FNProtocolFactory)
    lake = factory.SubFactory(LakeFactory)
    species = factory.SubFactory(SpeciesFactory)
    grp = "00"
    grp_des = "default group"
    biosam = "1"
    sizsam = 1
    sizatt = "FLEN"
    sizint = 1
    fdsam1 = "0"
    spcmrk1 = "0"
    agedec1 = "X"
    agedec2 = "0"
    flen_min = 150
    flen_max = 750
    tlen_min = 150
    tlen_max = 750
    rwt_min = 100
    rwt_max = 2500
    k_min_error = 0.2
    k_min_warn = 0.5
    k_max_error = 3.5
    k_max_warn = 3.0


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
    mesh = "038"
    grlen = "25"
    grht = "1.8"
    grcol = "G"
    grmat = "3"
    gryarn = "1"
    grknot = "2"


class FN022Factory(factory.django.DjangoModelFactory):
    """a factory for seasons"""

    class Meta:
        model = FN022
        django_get_or_create = ["project", "ssn"]

    project = factory.SubFactory(FN011Factory)
    ssn = factory.Sequence(lambda n: "{:02d}".format(n)[-2:])
    ssn_des = "Spring"

    @factory.lazy_attribute
    def ssn_date0(self):

        # datestring = "April 15, 2015"
        # ssn_date0 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        # return ssn_date0
        return self.project.prj_date0

    @factory.lazy_attribute
    def ssn_date1(self):
        return self.project.prj_date1
        # datestring = "June 15, 2015"
        # ssn_date1 = datetime.datetime.strptime(datestring, "%B %d, %Y")
        # return ssn_date1


class FN026Factory(factory.django.DjangoModelFactory):
    """a factory for spatial strata"""

    class Meta:
        model = FN026
        django_get_or_create = ["project", "space"]

    space = factory.Sequence(lambda n: "{:02d}".format(n)[-2:])
    space_des = "The Lake"
    project = factory.SubFactory(FN011Factory)


class FN028Factory(factory.django.DjangoModelFactory):
    """a factory for fishing modes"""

    class Meta:
        model = FN028
        django_get_or_create = ["project", "mode"]

    mode = factory.Sequence(lambda n: "{:02d}".format(n)[-2:])
    mode_des = "Gillnet 2-6 inch"
    project = factory.SubFactory(FN011Factory)
    gear = factory.SubFactory(GearFactory)
    orient = 2
    gruse = 1
