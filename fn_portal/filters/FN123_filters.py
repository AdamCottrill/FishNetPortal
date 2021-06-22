import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN123


class FN123SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn123 data only)"""

    grp = ValueInFilter(field_name="grp")
    spc = ValueInFilter(field_name="species__spc")

    class Meta:
        model = FN123
        fields = ["species__spc", "grp"]


class FN123Filter(FN123SubFilter):
    """A filter that is inherited from FN123SubFilter and allows
    additional filters based on attributes of the parent tables
    (project, net and effort Attributes).

    """

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="effort__eff")

    # net set attributes:

    sidep_gte = django_filters.NumberFilter(
        field_name="effort__sample__sidep", lookup_expr="gte"
    )
    sidep_lte = django_filters.NumberFilter(
        field_name="effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="effort__sample__grtp")
    gr = ValueInFilter(field_name="effort__sample__gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="effort__sample__grid__grid")

    effdur_gte = django_filters.NumberFilter(
        field_name="effort__sample__effdur", lookup_expr="gte"
    )
    effdur_lte = django_filters.NumberFilter(
        field_name="effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date_gte = django_filters.DateFilter(
        field_name="effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date_lte = django_filters.DateFilter(
        field_name="effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date_gte = django_filters.DateFilter(
        field_name="effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date_lte = django_filters.DateFilter(
        field_name="effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time_gte = django_filters.TimeFilter(
        field_name="effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time_lte = django_filters.TimeFilter(
        field_name="effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time_gte = django_filters.TimeFilter(
        field_name="effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time_lte = django_filters.TimeFilter(
        field_name="effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # project attributes
    year = django_filters.CharFilter(
        field_name="effort__sample__project__year", lookup_expr="exact"
    )
    first_year = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="lte"
    )

    protocol = ValueInFilter(field_name="effort__sample__project__protocol__abbrev")

    prj_cd = django_filters.CharFilter(field_name="effort__sample__project__prj_cd")

    prj_cd_in = ValueInFilter(field_name="effort__sample__project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="effort__sample__project__prj_cd", lookup_expr="icontains"
    )

    lake = django_filters.CharFilter(
        field_name="effort__sample__project__lake__abbrev", lookup_expr="iexact"
    )

    class Meta:
        model = FN123
        fields = ["species__spc", "grp"]
