import factory
import datetime

from .user_factory import UserFactory

from .common_factories import LakeFactory

from ...models import FNProtocol, FN011, FN013, FN014


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
