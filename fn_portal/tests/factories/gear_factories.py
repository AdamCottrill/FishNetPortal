from _pytest.recwarn import deprecated_call
import factory

from ...models import Gear, Gear2SubGear, GearFamily, SubGear, GearEffortProcessType


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
        django_get_or_create = ("gr_code",)

    family = factory.SubFactory(GearFamilyFactory)
    gr_label = "Monofilament Gillnet"
    gr_code = "GL10"
    grtp = "GL"
    gr_des = "This is a fake gear used for testing."
    depreciated = False
    confirmed = True


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
    mesh = 51
    grlen = 50
    grht = 1.8


class Gear2SubGearFactory(factory.django.DjangoModelFactory):
    """A factory for Gear2SubGear objects.  Only fields that are required or
    have been tested are currently inlcuded in this factory.

    """

    class Meta:
        model = Gear2SubGear
        # django_get_or_create = ("gear",)

    gear = factory.SubFactory(GearFactory)
    subgear = factory.SubFactory(SubGearFactory)


class GearEffortProcessTypeFactory(factory.django.DjangoModelFactory):
    """A factory for GearEffortProcessType objects."""

    class Meta:
        model = GearEffortProcessType
        django_get_or_create = ("gear", "eff", "process_type")

    gear = factory.SubFactory(GearFactory)
    eff = "001"
    process_type = "1"
    effdst = None
