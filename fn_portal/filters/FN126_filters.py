import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN126


class FN126SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of FN126 table (diet data) by
    by attributes of the diet items (fn126 data only)"""

    taxon_like = ValueInFilter(field_name="taxon", lookup_expr="icontains")
    taxon = ValueInFilter(field_name="taxon")

    foodcnt = django_filters.NumberFilter(field_name="foodcnt")
    foodcnt_gte = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="gte")
    foodcnt_lte = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="lte")

    foodcnt_gt = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="gt")
    foodcnt_lt = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="lt")

    class Meta:
        model = FN126
        fields = ["taxon"]


class FN126Filter(FN126SubFilter):
    """A fitlerset that allows us to select subsets of tags objects
    by attributes of the tag data as well as the parent tables:
    net set, effort, catch and fish attributes.

    """

    # catch attributes:
    grp = ValueInFilter(field_name="fish__catch__grp")
    spc = ValueInFilter(field_name="fish__catch__species__spc")

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="fish__catch__effort__eff")

    # net set attributes:

    sidep_gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="gte"
    )
    sidep_lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="fish__catch__effort__sample__grtp")
    gr = ValueInFilter(field_name="fish__catch__effort__sample__gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="fish__catch__effort__sample__grid__grid")

    effdur_gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__effdur", lookup_expr="gte"
    )
    effdur_lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date_gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date_lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date_gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date_lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time_gte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time_lte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time_gte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time_lte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # project attributes
    year = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="exact"
    )
    first_year = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="lte"
    )

    protocol = ValueInFilter(
        field_name="fish__catch__effort__sample__project__protocol__abbrev"
    )

    prj_cd = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd"
    )

    prj_cd_in = ValueInFilter(field_name="fish__catch__effort__sample__project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
    )

    lake = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__lake__abbrev",
        lookup_expr="iexact",
    )

    class Meta:
        model = FN126
        fields = ["taxon", "foodcnt"]
