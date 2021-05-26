import factory


from common.models import Species, Lake, Grid5


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
