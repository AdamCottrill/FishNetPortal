import factory

from ...models import (
    FN121,
    FN121Limno,
    FN121Weather,
    FN121Trapnet,
    FN122,
    FN123,
    FN124,
    FN125,
    FN126,
    FN127,
    FN125_Lamprey,
    FN125Tag,
)
from .FN0_factories import (
    FN011Factory,
    FN022Factory,
    FN026SubspaceFactory,
    FN028Factory,
)
from .common_factories import Grid5Factory, BottomTypeFactory, CoverTypeFactory


class FN121Factory(factory.django.DjangoModelFactory):
    """A factory for FN121 objects.  Only fields that are required or have
    been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = FN121
        django_get_or_create = ("project", "sam")

    project = factory.SubFactory(FN011Factory)
    sam = factory.Sequence(lambda n: "{:03d}".format(n))

    ssn = factory.SubFactory(FN022Factory, __sequence=1)
    subspace = factory.SubFactory(FN026SubspaceFactory, __sequence=1)
    mode = factory.SubFactory(FN028Factory, __sequence=1)
    grid5 = factory.SubFactory(Grid5Factory, __sequence=1)


class FN121LimnoFactory(factory.django.DjangoModelFactory):
    """A factory for FN121Limno objects - individual water chemistry
    values that may or may not be collected depending on the project.
    1:1 relationshop with FN121 objects."""

    class Meta:
        model = FN121Limno
        django_get_or_create = ("sample",)

    sample = factory.SubFactory(FN121Factory)

    o2gear0 = 12.0
    o2gear1 = 12.5
    o2bot0 = 11.0
    o2bot1 = 11.0
    o2surf0 = 14.0
    o2surf1 = 14.0


class FN121WeatherFactory(factory.django.DjangoModelFactory):
    """A factory for FN121Weather objects - individual weather
    conditions at the start and end of a smampling event.  Weather
    attributes may or may not be collected depending on the project.
    They have a 1:1 relationshop with FN121 objects.

    """

    class Meta:
        model = FN121Weather
        django_get_or_create = ("sample",)

    sample = factory.SubFactory(FN121Factory)

    airtem0 = 11.2
    airtem1 = 9.8
    wind_speed0 = 10
    wind_speed1 = 5
    wind_direction0 = 90
    wind_direction1 = 270
    precip0 = "40"
    precip1 = "00"
    # cloud_pc0 = 20
    # cloud_pc1 = 80
    # waveht0 = 0.1
    # waveht1 = 0.3
    precip_duration = 1
    wave_duration = 2


class FN121TrapnetFactory(factory.django.DjangoModelFactory):
    """A factory for FN121Trapnet objects - individual trapnet
    attributes.  Trapnet attributes may or may not be collected
    depending on the project.  They have a 1:1 relationshop with FN121
    objects.

    """

    class Meta:
        model = FN121Trapnet
        django_get_or_create = ("sample",)

    sample = factory.SubFactory(FN121Factory)
    bottom = factory.SubFactory(BottomTypeFactory)
    cover = factory.SubFactory(CoverTypeFactory)

    vegetation = 1
    lead_angle = 90
    leaduse = 25
    distoff = 0


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
    grp = "00"


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
    fdcnt = 6


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
