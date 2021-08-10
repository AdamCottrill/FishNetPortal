import factory

from ...models import Gear, Gear2SubGear, GearFamily, SubGear


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
