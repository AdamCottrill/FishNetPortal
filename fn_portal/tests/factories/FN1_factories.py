import factory


from .FN0_factories import FN011Factory

from ...models import (
    FN121,
    FN122,
    FN123,
    FN124,
    FN125,
    FN127,
    FN126,
    FN125Tag,
    FN125_Lamprey,
)


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


class FN124Factory(factory.django.DjangoModelFactory):
    """A factory for FN124 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN124
        django_get_or_create = ("catch", "siz")

    catch = factory.SubFactory(FN123Factory)
    siz = 350
    sizcnt = 12


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
