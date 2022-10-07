import factory
from django.contrib.gis.geos import GEOSGeometry

from common.models import Species, Lake, Grid5, CoverType, BottomType, Vessel


wkt = (
    "MULTIPOLYGON(((-82.000 43.999,"
    + "-82.083 43.999,"
    + "-82.083 44.083,"
    + "-82.000 44.083,"
    + "-82.000 43.999)))"
)


class LakeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Lake
        django_get_or_create = ("abbrev",)

    lake_name = "Lake Huron"
    abbrev = "HU"
    geom_ontario = GEOSGeometry(wkt.replace("\n", ""), srid=4326)


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


class BottomTypeFactory(factory.django.DjangoModelFactory):
    """
    A factory for bottom types.
    """

    class Meta:
        model = BottomType
        django_get_or_create = ("abbrev",)

    abbrev = "BO"
    label = "Boulder"
    obsolete_date = None


class CoverTypeFactory(factory.django.DjangoModelFactory):
    """
    A factory for cover types.
    """

    class Meta:
        model = CoverType
        django_get_or_create = ("abbrev",)

    abbrev = "MA"
    label = "Macrophytes"
    obsolete_date = None


class VesselFactory(factory.django.DjangoModelFactory):
    """
    A factory for Vessels.
    """

    class Meta:
        model = Vessel
        django_get_or_create = ("abbrev",)

    abbrev = "RV-OE"
    label = "Ontario Explorer"
    obsolete_date = None
