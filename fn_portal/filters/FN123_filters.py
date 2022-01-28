import django_filters

from .common_filters import ValueInFilter, NumberInFilter, GeoFilterSet, GeomFilter

from ..models import FN123


class FN123SubFilter(GeoFilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn123 data only)"""

    roi = GeomFilter(field_name="effort__sample__geom__within", method="filter_roi")

    buffered_point = GeomFilter(
        field_name="effort__sample__geom__within", method="filter_point"
    )

    management_unit__in = ValueInFilter(
        field_name="effort__sample__management_units__slug"
    )
    management_unit__not__in = ValueInFilter(
        field_name="effort__sample__management_units__slug", exclude=True
    )

    grp = ValueInFilter(field_name="grp")
    grp__not = ValueInFilter(field_name="grp", exclude=True)

    spc = ValueInFilter(field_name="species__spc")
    spc__not = ValueInFilter(field_name="species__spc", exclude=True)

    catcnt = django_filters.NumberFilter(field_name="catcnt", lookup_expr="exact")
    catcnt__gte = django_filters.NumberFilter(field_name="catcnt", lookup_expr="gte")
    catcnt__lte = django_filters.NumberFilter(field_name="catcnt", lookup_expr="lte")
    catcnt__gt = django_filters.NumberFilter(field_name="catcnt", lookup_expr="gt")
    catcnt__lt = django_filters.NumberFilter(field_name="catcnt", lookup_expr="lt")

    biocnt = django_filters.NumberFilter(field_name="biocnt", lookup_expr="exact")
    biocnt__gte = django_filters.NumberFilter(field_name="biocnt", lookup_expr="gte")
    biocnt__lte = django_filters.NumberFilter(field_name="biocnt", lookup_expr="lte")
    biocnt__gt = django_filters.NumberFilter(field_name="biocnt", lookup_expr="gt")
    biocnt__lt = django_filters.NumberFilter(field_name="biocnt", lookup_expr="lt")

    class Meta:
        model = FN123
        fields = ["species__spc", "grp"]


class FN123Filter(FN123SubFilter):
    """A filter that is inherited from FN123SubFilter and allows
    additional filters based on attributes of the parent tables
    (project, net and effort Attributes).

    """

    # FN011 ATTRIBUTES
    year = django_filters.CharFilter(
        field_name="effort__sample__project__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="lte"
    )
    year__gt = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="effort__sample__project__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="effort__sample__project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="effort__sample__project__prj_cd")
    prj_cd__not = ValueInFilter(
        field_name="effort__sample__project__prj_cd", exclude=True
    )

    prj_cd__like = django_filters.CharFilter(
        field_name="effort__sample__project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="effort__sample__project__prj_cd",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="effort__sample__project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="effort__sample__project__prj_cd",
        lookup_expr="endswith",
        exclude=True,
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="effort__sample__project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="effort__sample__project__prj_nm",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_ldr = django_filters.CharFilter(
        field_name="effort__sample__project__prj_ldr__username", lookup_expr="iexact"
    )

    protocol = ValueInFilter(field_name="effort__sample__project__protocol__abbrev")
    protocol__not = ValueInFilter(
        field_name="effort__sample__project__protocol__abbrev", exclude=True
    )

    lake = ValueInFilter(field_name="effort__sample__project__lake__abbrev")

    lake__not = ValueInFilter(
        field_name="effort__sample__project__lake__abbrev", exclude=True
    )

    # FN121 ATTRIBUTES

    sam = ValueInFilter(field_name="effort__sample__sam")
    sam__not = ValueInFilter(field_name="effort__sample__sam", exclude=True)

    sidep__gte = django_filters.NumberFilter(
        field_name="effort__sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="effort__sample__mode__gear__grtp")
    grtp__not = ValueInFilter(
        field_name="effort__sample__mode__gear__grtp", exclude=True
    )

    gr = ValueInFilter(field_name="effort__sample__mode__gear__gr_code")
    gr__not = ValueInFilter(
        field_name="effort__sample__mode__gear__gr_code", exclude=True
    )

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="effort__sample__grid__grid")
    grid__not = NumberInFilter(field_name="effort__sample__grid__grid", exclude=True)

    effdur__gte = django_filters.NumberFilter(
        field_name="effort__sample__effdur", lookup_expr="gte"
    )
    effdur__lte = django_filters.NumberFilter(
        field_name="effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date__gte = django_filters.DateFilter(
        field_name="effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date__lte = django_filters.DateFilter(
        field_name="effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date__gte = django_filters.DateFilter(
        field_name="effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date__lte = django_filters.DateFilter(
        field_name="effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time__gte = django_filters.TimeFilter(
        field_name="effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time__lte = django_filters.TimeFilter(
        field_name="effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time__gte = django_filters.TimeFilter(
        field_name="effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time__lte = django_filters.TimeFilter(
        field_name="effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # FN122 ATTRIBUTES

    eff = ValueInFilter(field_name="effort__eff")
    eff__not = ValueInFilter(field_name="effort__eff", exclude=True)

    effdst = django_filters.NumberFilter(
        field_name="effort__effdst", lookup_expr="exact"
    )
    effdst__gte = django_filters.NumberFilter(
        field_name="effort__effdst", lookup_expr="gte"
    )
    effdst__lte = django_filters.NumberFilter(
        field_name="effort__effdst", lookup_expr="lte"
    )
    effdst__gt = django_filters.NumberFilter(
        field_name="effort__effdst", lookup_expr="gt"
    )
    effdst__lt = django_filters.NumberFilter(
        field_name="effort__effdst", lookup_expr="lt"
    )

    grdep = django_filters.NumberFilter(field_name="effort__grdep", lookup_expr="exact")
    grdep__gte = django_filters.NumberFilter(
        field_name="effort__grdep", lookup_expr="gte"
    )
    grdep__lte = django_filters.NumberFilter(
        field_name="effort__grdep", lookup_expr="lte"
    )
    grdep__gt = django_filters.NumberFilter(
        field_name="effort__grdep", lookup_expr="gt"
    )
    grdep__lt = django_filters.NumberFilter(
        field_name="effort__grdep", lookup_expr="lt"
    )

    grtem0 = django_filters.NumberFilter(
        field_name="effort__grtem0", lookup_expr="exact"
    )
    grtem0__gte = django_filters.NumberFilter(
        field_name="effort__grtem0", lookup_expr="gte"
    )
    grtem0__lte = django_filters.NumberFilter(
        field_name="effort__grtem0", lookup_expr="lte"
    )
    grtem0__gt = django_filters.NumberFilter(
        field_name="effort__grtem0", lookup_expr="gt"
    )
    grtem0__lt = django_filters.NumberFilter(
        field_name="effort__grtem0", lookup_expr="lt"
    )

    grtem1 = django_filters.NumberFilter(
        field_name="effort__grtem1", lookup_expr="exact"
    )
    grtem1__gte = django_filters.NumberFilter(
        field_name="effort__grtem1", lookup_expr="gte"
    )
    grtem1__lte = django_filters.NumberFilter(
        field_name="effort__grtem1", lookup_expr="lte"
    )
    grtem1__gt = django_filters.NumberFilter(
        field_name="effort__grtem1", lookup_expr="gt"
    )
    grtem1__lt = django_filters.NumberFilter(
        field_name="effort__grtem1", lookup_expr="lt"
    )

    class Meta:
        model = FN123
        fields = ["species__spc", "grp"]
