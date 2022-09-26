import django_filters

from .common_filters import ValueInFilter, NumberInFilter, GeoFilterSet, GeomFilter

from ..models import FN121Limno


class FN121LimnoInProjectFilter(GeoFilterSet):
    """A fitlerset that allows us to select subsets of limnological databy
    by spatial attributes or water chemistry (ie. limno data only)"""

    roi = GeomFilter(field_name="sample__geom__within", method="filter_roi")

    buffered_point = GeomFilter(
        field_name="sample__geom__within", method="filter_point"
    )

    management_unit__in = ValueInFilter(field_name="sample__management_units__slug")
    management_unit__not__in = ValueInFilter(
        field_name="sample__management_units__slug", exclude=True
    )

    o2gear0 = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="exact")
    o2gear0__gte = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="gte")
    o2gear0__lte = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="lte")
    o2gear0__gt = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="gt")
    o2gear0__lt = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="lt")
    o2gear0__null = django_filters.BooleanFilter(
        field_name="o2gear0", lookup_expr="isnull"
    )
    o2gear0__not_null = django_filters.BooleanFilter(
        field_name="o2gear0", lookup_expr="isnull", exclude=True
    )

    o2gear1 = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="exact")
    o2gear1__gte = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="gte")
    o2gear1__lte = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="lte")
    o2gear1__gt = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="gt")
    o2gear1__lt = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="lt")
    o2gear1__null = django_filters.BooleanFilter(
        field_name="o2gear1", lookup_expr="isnull"
    )
    o2gear1__not_null = django_filters.BooleanFilter(
        field_name="o2gear1", lookup_expr="isnull", exclude=True
    )

    o2bot0 = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="exact")
    o2bot0__gte = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="gte")
    o2bot0__lte = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="lte")
    o2bot0__gt = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="gt")
    o2bot0__lt = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="lt")
    o2bot0__null = django_filters.BooleanFilter(
        field_name="o2bot0", lookup_expr="isnull"
    )
    o2bot0__not_null = django_filters.BooleanFilter(
        field_name="o2bot0", lookup_expr="isnull", exclude=True
    )

    o2bot1 = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="exact")
    o2bot1__gte = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="gte")
    o2bot1__lte = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="lte")
    o2bot1__gt = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="gt")
    o2bot1__lt = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="lt")
    o2bot1__null = django_filters.BooleanFilter(
        field_name="o2bot1", lookup_expr="isnull"
    )
    o2bot1__not_null = django_filters.BooleanFilter(
        field_name="o2bot1", lookup_expr="isnull", exclude=True
    )

    o2surf0 = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="exact")
    o2surf0__gte = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="gte")
    o2surf0__lte = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="lte")
    o2surf0__gt = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="gt")
    o2surf0__lt = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="lt")
    o2surf0__null = django_filters.BooleanFilter(
        field_name="o2surf0", lookup_expr="isnull"
    )
    o2surf0__not_null = django_filters.BooleanFilter(
        field_name="o2surf0", lookup_expr="isnull", exclude=True
    )

    o2surf1 = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="exact")
    o2surf1__gte = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="gte")
    o2surf1__lte = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="lte")
    o2surf1__gt = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="gt")
    o2surf1__lt = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="lt")
    o2surf1__null = django_filters.BooleanFilter(
        field_name="o2surf1", lookup_expr="isnull"
    )
    o2surf1__not_null = django_filters.BooleanFilter(
        field_name="o2surf1", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = FN121Limno
        fields = [
            "o2gear0",
            "o2bot0",
            "o2bot1",
            "o2surf0",
            "o2surf1",
        ]


class FN121LimnoFilter(FN121LimnoInProjectFilter):
    """A filter that is inherited from FN121LimnoInProjectFilter and allows
    additional filters based on attributes of the parent tables
    (project and net set attributes).
    """

    # FN011 attributes
    year = django_filters.CharFilter(
        field_name="sample__project__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="sample__project__prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="sample__project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="sample__project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="sample__project__prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="sample__project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="sample__project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="sample__project__prj_cd")
    prj_cd__not = ValueInFilter(field_name="sample__project__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="sample__project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="sample__project__prj_nm", lookup_expr="icontains", exclude=True
    )

    prj_ldr = django_filters.CharFilter(
        field_name="sample__project__prj_ldr__username", lookup_expr="iexact"
    )

    protocol = ValueInFilter(field_name="sample__project__protocol__abbrev")
    protocol__not = ValueInFilter(
        field_name="sample__project__protocol__abbrev", exclude=True
    )

    lake = ValueInFilter(field_name="sample__project__lake__abbrev")

    lake__not = ValueInFilter(field_name="sample__project__lake__abbrev", exclude=True)

    # FN121 Attributes

    sam = ValueInFilter(field_name="sample__sam")
    sam__not = ValueInFilter(field_name="sample__sam", exclude=True)

    sidep__gte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="sample__mode__gear__grtp")
    grtp__not = ValueInFilter(field_name="sample__mode__gear__grtp", exclude=True)

    gr = ValueInFilter(field_name="sample__mode__gear__gr_code")
    gr__not = ValueInFilter(field_name="sample__mode__gear__gr_code", exclude=True)

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="sample__grid__grid")
    grid__not = NumberInFilter(field_name="sample__grid__grid", exclude=True)

    effdur__gte = django_filters.NumberFilter(
        field_name="sample__effdur", lookup_expr="gte"
    )
    effdur__lte = django_filters.NumberFilter(
        field_name="sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date__gte = django_filters.DateFilter(
        field_name="sample__effdt0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    set_date__lte = django_filters.DateFilter(
        field_name="sample__effdt0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    lift_date = django_filters.DateFilter(
        field_name="sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date__gte = django_filters.DateFilter(
        field_name="sample__effdt1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    lift_date__lte = django_filters.DateFilter(
        field_name="sample__effdt1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    set_time = django_filters.TimeFilter(
        field_name="sample__efftm0", help_text="format: HH:MM"
    )
    set_time__gte = django_filters.TimeFilter(
        field_name="sample__efftm0", lookup_expr="gte", help_text="format: HH:MM"
    )
    set_time__lte = django_filters.TimeFilter(
        field_name="sample__efftm0", lookup_expr="lte", help_text="format: HH:MM"
    )

    lift_time = django_filters.TimeFilter(
        field_name="sample__efftm1", help_text="format: HH:MM"
    )
    lift_time__gte = django_filters.TimeFilter(
        field_name="sample__efftm1", lookup_expr="gte", help_text="format: HH:MM"
    )
    lift_time__lte = django_filters.TimeFilter(
        field_name="sample__efftm1", lookup_expr="lte", help_text="format: HH:MM"
    )

    class Meta:
        model = FN121Limno
        fields = [
            "o2gear0",
            "o2bot0",
            "o2bot1",
            "o2surf0",
            "o2surf1",
        ]
