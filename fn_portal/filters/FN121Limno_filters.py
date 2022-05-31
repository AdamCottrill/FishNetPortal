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

    do_gear = django_filters.NumberFilter(field_name="do_gear", lookup_expr="exact")
    do_gear__gte = django_filters.NumberFilter(field_name="do_gear", lookup_expr="gte")
    do_gear__lte = django_filters.NumberFilter(field_name="do_gear", lookup_expr="lte")
    do_gear__gt = django_filters.NumberFilter(field_name="do_gear", lookup_expr="gt")
    do_gear__lt = django_filters.NumberFilter(field_name="do_gear", lookup_expr="lt")
    do_gear__null = django_filters.BooleanFilter(
        field_name="do_gear", lookup_expr="isnull"
    )
    do_gear__not_null = django_filters.BooleanFilter(
        field_name="do_gear", lookup_expr="isnull", exclude=True
    )

    xo2 = django_filters.NumberFilter(field_name="xo2", lookup_expr="exact")
    xo2__gte = django_filters.NumberFilter(field_name="xo2", lookup_expr="gte")
    xo2__lte = django_filters.NumberFilter(field_name="xo2", lookup_expr="lte")
    xo2__gt = django_filters.NumberFilter(field_name="xo2", lookup_expr="gt")
    xo2__lt = django_filters.NumberFilter(field_name="xo2", lookup_expr="lt")
    xo2__null = django_filters.BooleanFilter(field_name="xo2", lookup_expr="isnull")
    xo2__not_null = django_filters.BooleanFilter(
        field_name="xo2", lookup_expr="isnull", exclude=True
    )

    xo22 = django_filters.NumberFilter(field_name="xo22", lookup_expr="exact")
    xo22__gte = django_filters.NumberFilter(field_name="xo22", lookup_expr="gte")
    xo22__lte = django_filters.NumberFilter(field_name="xo22", lookup_expr="lte")
    xo22__gt = django_filters.NumberFilter(field_name="xo22", lookup_expr="gt")
    xo22__lt = django_filters.NumberFilter(field_name="xo22", lookup_expr="lt")
    xo22__null = django_filters.BooleanFilter(field_name="xo22", lookup_expr="isnull")
    xo22__not_null = django_filters.BooleanFilter(
        field_name="xo22", lookup_expr="isnull", exclude=True
    )

    surfdo2 = django_filters.NumberFilter(field_name="surfdo2", lookup_expr="exact")
    surfdo2__gte = django_filters.NumberFilter(field_name="surfdo2", lookup_expr="gte")
    surfdo2__lte = django_filters.NumberFilter(field_name="surfdo2", lookup_expr="lte")
    surfdo2__gt = django_filters.NumberFilter(field_name="surfdo2", lookup_expr="gt")
    surfdo2__lt = django_filters.NumberFilter(field_name="surfdo2", lookup_expr="lt")
    surfdo2__null = django_filters.BooleanFilter(
        field_name="surfdo2", lookup_expr="isnull"
    )
    surfdo2__not_null = django_filters.BooleanFilter(
        field_name="surfdo2", lookup_expr="isnull", exclude=True
    )

    surfdo22 = django_filters.NumberFilter(field_name="surfdo22", lookup_expr="exact")
    surfdo22__gte = django_filters.NumberFilter(
        field_name="surfdo22", lookup_expr="gte"
    )
    surfdo22__lte = django_filters.NumberFilter(
        field_name="surfdo22", lookup_expr="lte"
    )
    surfdo22__gt = django_filters.NumberFilter(field_name="surfdo22", lookup_expr="gt")
    surfdo22__lt = django_filters.NumberFilter(field_name="surfdo22", lookup_expr="lt")
    surfdo22__null = django_filters.BooleanFilter(
        field_name="surfdo22", lookup_expr="isnull"
    )
    surfdo22__not_null = django_filters.BooleanFilter(
        field_name="surfdo22", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = FN121Limno
        fields = [
            "do_gear",
            "xo2",
            "xo22",
            "surfdo2",
            "surfdo22",
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
            "do_gear",
            "xo2",
            "xo22",
            "surfdo2",
            "surfdo22",
        ]
