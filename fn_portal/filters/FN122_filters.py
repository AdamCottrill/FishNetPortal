import django_filters

from .common_filters import ValueInFilter, NumberInFilter, GeoFilterSet, GeomFilter

from ..models import FN122, FN122Transect


class FN122SubFilter(GeoFilterSet):
    """A fitlerset that allows us to select subsets objects by
    by attributes of the project and sample - objects related to the FN121 table."""

    roi = GeomFilter(field_name="sample__geom__within", method="filter_roi")

    buffered_point = GeomFilter(
        field_name="sample__geom__within", method="filter_point"
    )

    management_unit__in = ValueInFilter(field_name="sample__management_units__slug")
    management_unit__not__in = ValueInFilter(
        field_name="sample__management_units__slug", exclude=True
    )

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
        model = FN122
        fields = ["eff"]


class FN122Filter(FN122SubFilter):
    """A filter that is inherited from FN122SubFilter and allows
    additional filters based on attributes of the effort itself.
    """

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="eff")
    eff_not = ValueInFilter(field_name="eff", exclude=True)

    effdst = django_filters.NumberFilter(field_name="effdst", lookup_expr="exact")
    effdst__gte = django_filters.NumberFilter(field_name="effdst", lookup_expr="gte")
    effdst__lte = django_filters.NumberFilter(field_name="effdst", lookup_expr="lte")
    effdst__gt = django_filters.NumberFilter(field_name="effdst", lookup_expr="gt")
    effdst__lt = django_filters.NumberFilter(field_name="effdst", lookup_expr="lt")

    grdep0 = django_filters.NumberFilter(field_name="grdep0", lookup_expr="exact")
    grdep0__gte = django_filters.NumberFilter(field_name="grdep0", lookup_expr="gte")
    grdep0__lte = django_filters.NumberFilter(field_name="grdep0", lookup_expr="lte")
    grdep0__gt = django_filters.NumberFilter(field_name="grdep0", lookup_expr="gt")
    grdep0__lt = django_filters.NumberFilter(field_name="grdep0", lookup_expr="lt")

    grdep1 = django_filters.NumberFilter(field_name="grdep1", lookup_expr="exact")
    grdep1__gte = django_filters.NumberFilter(field_name="grdep1", lookup_expr="gte")
    grdep1__lte = django_filters.NumberFilter(field_name="grdep1", lookup_expr="lte")
    grdep1__gt = django_filters.NumberFilter(field_name="grdep1", lookup_expr="gt")
    grdep1__lt = django_filters.NumberFilter(field_name="grdep1", lookup_expr="lt")

    grtem0 = django_filters.NumberFilter(field_name="grtem0", lookup_expr="exact")
    grtem0__gte = django_filters.NumberFilter(field_name="grtem0", lookup_expr="gte")
    grtem0__lte = django_filters.NumberFilter(field_name="grtem0", lookup_expr="lte")
    grtem0__gt = django_filters.NumberFilter(field_name="grtem0", lookup_expr="gt")
    grtem0__lt = django_filters.NumberFilter(field_name="grtem0", lookup_expr="lt")

    grtem1 = django_filters.NumberFilter(field_name="grtem1", lookup_expr="exact")
    grtem1__gte = django_filters.NumberFilter(field_name="grtem1", lookup_expr="gte")
    grtem1__lte = django_filters.NumberFilter(field_name="grtem1", lookup_expr="lte")
    grtem1__gt = django_filters.NumberFilter(field_name="grtem1", lookup_expr="gt")
    grtem1__lt = django_filters.NumberFilter(field_name="grtem1", lookup_expr="lt")

    class Meta:
        model = FN122
        fields = ["eff"]


class FN122TransectFilter(FN122SubFilter):
    """A filter that is inherited from FN122SubFilter and allows
    additional filters based on attributes of the transect point itself.
    """

    transect_sidep = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="exact"
    )
    transect_sidep__gte = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="gte"
    )
    transect_sidep__lte = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="lte"
    )
    transect_sidep__gt = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="gt"
    )
    transect_sidep__lt = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="lt"
    )

    # allow us to filter by and between dates using one or both of:
    # timestamp_date_before and timestamp_date_after
    # ignores the time:
    timestamp_date = django_filters.DateFromToRangeFilter()

    timestamp__gte = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    timestamp__lte = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lte"
    )
    timestamp__gt = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gt"
    )
    timestamp__lt = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lt"
    )

    # these will be applied to the geom of transect record:
    transect_roi = GeomFilter(field_name="geom__within", method="filter_roi")
    transect_buffered_point = GeomFilter(
        field_name="geom__within", method="filter_point"
    )

    class Meta:
        model = FN122Transect
        fields = ["sidep", "timestamp"]
