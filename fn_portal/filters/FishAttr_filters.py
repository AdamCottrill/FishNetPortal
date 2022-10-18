import django_filters

from .common_filters import NumberInFilter, ValueInFilter, GeomFilter, GeoFilterSet


class FishAttrFilters(GeoFilterSet):
    """A filter set that contains filters that are common to all the FN125 child
    tables - FN125Lamprey, FN125Tag, Fn126, and FN127.  Filtersets for those class
    inherit from this one, and add their own models and model specific filters.

    Filters in this class include filters from FN011 to FN125 Tables.

    """

    roi = GeomFilter(
        field_name="fish__catch__effort__sample__geom__within", method="filter_roi"
    )

    buffered_point = GeomFilter(
        field_name="fish__catch__effort__sample__geom__within", method="filter_point"
    )

    management_unit__in = ValueInFilter(
        field_name="fish__catch__effort__sample__management_units__slug"
    )
    management_unit__not__in = ValueInFilter(
        field_name="fish__catch__effort__sample__management_units__slug", exclude=True
    )

    # FN011 (PROJECT) ATTRIBUTES

    year = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="lte"
    )
    year__gt = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__project__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date0",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date1",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="fish__catch__effort__sample__project__prj_cd")
    prj_cd__not = ValueInFilter(
        field_name="fish__catch__effort__sample__project__prj_cd", exclude=True
    )

    prj_cd__like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="endswith",
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="endswith",
        exclude=True,
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_nm",
        lookup_expr="icontains",
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_nm",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_ldr = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_ldr__username",
        lookup_expr="iexact",
    )

    protocol = ValueInFilter(
        field_name="fish__catch__effort__sample__project__protocol__abbrev"
    )

    protocol__not = ValueInFilter(
        field_name="fish__catch__effort__sample__project__protocol__abbrev",
        exclude=True,
    )

    lake = ValueInFilter(
        field_name="fish__catch__effort__sample__project__lake__abbrev",
    )

    lake__not = ValueInFilter(
        field_name="fish__catch__effort__sample__project__lake__abbrev", exclude=True
    )

    # FN121 (NET SET) ATTRIBUTES:

    sam = ValueInFilter(field_name="fish__catch__effort__sample__sam")
    sam__not = ValueInFilter(
        field_name="fish__catch__effort__sample__sam", exclude=True
    )

    sidep__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="fish__catch__effort__sample__mode__gear__grtp")
    grtp__not = ValueInFilter(
        field_name="fish__catch__effort__sample__mode__gear__grtp", exclude=True
    )

    gr = ValueInFilter(field_name="fish__catch__effort__sample__mode__gear__gr_code")
    gr__not = ValueInFilter(
        field_name="fish__catch__effort__sample__mode__gear__gr_code", exclude=True
    )

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="fish__catch__effort__sample__grid__grid")
    grid__not = NumberInFilter(
        field_name="fish__catch__effort__sample__grid__grid", exclude=True
    )

    effdur__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__effdur", lookup_expr="gte"
    )
    effdur__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date__gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date__lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date__gte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date__lte = django_filters.DateFilter(
        field_name="fish__catch__effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time__gte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time__lte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time__gte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time__lte = django_filters.TimeFilter(
        field_name="fish__catch__effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # FN122 (EFFORT) ATTRIBUTES

    eff = ValueInFilter(field_name="fish__catch__effort__eff")
    eff__not = ValueInFilter(field_name="fish__catch__effort__eff", exclude=True)

    effdst = django_filters.NumberFilter(
        field_name="fish__catch__effort__effdst", lookup_expr="exact"
    )
    effdst__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__effdst", lookup_expr="gte"
    )
    effdst__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__effdst", lookup_expr="lte"
    )
    effdst__gt = django_filters.NumberFilter(
        field_name="fish__catch__effort__effdst", lookup_expr="gt"
    )
    effdst__lt = django_filters.NumberFilter(
        field_name="fish__catch__effort__effdst", lookup_expr="lt"
    )

    grdep = django_filters.NumberFilter(
        field_name="fish__catch__effort__grdep", lookup_expr="exact"
    )
    grdep__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grdep", lookup_expr="gte"
    )
    grdep__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grdep", lookup_expr="lte"
    )
    grdep__gt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grdep", lookup_expr="gt"
    )
    grdep__lt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grdep", lookup_expr="lt"
    )

    grtem0 = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem0", lookup_expr="exact"
    )
    grtem0__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem0", lookup_expr="gte"
    )
    grtem0__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem0", lookup_expr="lte"
    )
    grtem0__gt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem0", lookup_expr="gt"
    )
    grtem0__lt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem0", lookup_expr="lt"
    )

    grtem1 = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem1", lookup_expr="exact"
    )
    grtem1__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem1", lookup_expr="gte"
    )
    grtem1__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem1", lookup_expr="lte"
    )
    grtem1__gt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem1", lookup_expr="gt"
    )
    grtem1__lt = django_filters.NumberFilter(
        field_name="fish__catch__effort__grtem1", lookup_expr="lt"
    )

    # FN123 (CATCH) ATTRIBUTES:

    grp = ValueInFilter(field_name="fish__catch__grp")
    grp__not = ValueInFilter(field_name="fish__catch__grp", exclude=True)

    spc = ValueInFilter(field_name="fish__catch__species__spc")
    spc__not = ValueInFilter(field_name="fish__catch__species__spc", exclude=True)

    catcnt = django_filters.NumberFilter(
        field_name="fish__catch__catcnt", lookup_expr="exact"
    )
    catcnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__catcnt", lookup_expr="gte"
    )
    catcnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__catcnt", lookup_expr="lte"
    )
    catcnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__catcnt", lookup_expr="gt"
    )
    catcnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__catcnt", lookup_expr="lt"
    )

    biocnt = django_filters.NumberFilter(
        field_name="fish__catch__biocnt", lookup_expr="exact"
    )
    biocnt__gte = django_filters.NumberFilter(
        field_name="fish__catch__biocnt", lookup_expr="gte"
    )
    biocnt__lte = django_filters.NumberFilter(
        field_name="fish__catch__biocnt", lookup_expr="lte"
    )
    biocnt__gt = django_filters.NumberFilter(
        field_name="fish__catch__biocnt", lookup_expr="gt"
    )
    biocnt__lt = django_filters.NumberFilter(
        field_name="fish__catch__biocnt", lookup_expr="lt"
    )
    # FN125 (FISH) ATTRIBUTES:
    tlen = django_filters.NumberFilter(field_name="fish__tlen")
    tlen__gte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="gte")
    tlen__lte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="lte")
    tlen__gt = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="gt")
    tlen__lt = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="lt")

    flen = django_filters.NumberFilter(field_name="fish__flen")
    flen__gte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="gte")
    flen__lte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="lte")
    flen__gt = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="gt")
    flen__lt = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="lt")

    rwt = django_filters.NumberFilter(field_name="fish__rwt")
    rwt__null = django_filters.BooleanFilter(
        field_name="fish__rwt", lookup_expr="isnull"
    )
    rwt__gte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="gte")
    rwt__lte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="lte")
    rwt__gt = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="gt")
    rwt__lt = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="lt")

    eviswt = django_filters.NumberFilter(field_name="fish__eviswt")
    eviswt__null = django_filters.BooleanFilter(
        field_name="fish__eviswt", lookup_expr="isnull"
    )

    eviswt__gte = django_filters.NumberFilter(
        field_name="fish__eviswt", lookup_expr="gte"
    )
    eviswt__lte = django_filters.NumberFilter(
        field_name="fish__eviswt", lookup_expr="lte"
    )
    eviswt__gt = django_filters.NumberFilter(
        field_name="fish__eviswt", lookup_expr="gt"
    )
    eviswt__lt = django_filters.NumberFilter(
        field_name="fish__eviswt", lookup_expr="lt"
    )

    mat = ValueInFilter(field_name="fish__mat")
    mat__not = ValueInFilter(field_name="fish__mat", exclude=True)
    mat__null = django_filters.BooleanFilter(
        field_name="fish__mat", lookup_expr="isnull"
    )

    gon = ValueInFilter(field_name="fish__gon")
    gon__not = ValueInFilter(field_name="fish__gon", exclude=True)
    gon__null = django_filters.BooleanFilter(
        field_name="fish__gon", lookup_expr="isnull"
    )

    sex = ValueInFilter(field_name="fish__sex")
    sex__not = ValueInFilter(field_name="fish__sex", exclude=True)
    sex__null = django_filters.BooleanFilter(
        field_name="fish__sex", lookup_expr="isnull"
    )

    clipc = ValueInFilter(field_name="fish__clipc")
    clipc__not = ValueInFilter(field_name="fish__clipc", exclude=True)
    clipc__null = django_filters.BooleanFilter(
        field_name="fish__clipc", lookup_expr="isnull"
    )
    clipc__like = django_filters.CharFilter(
        field_name="fish__clipc", lookup_expr="icontains"
    )
    clipc__not_like = django_filters.CharFilter(
        field_name="fish__clipc", lookup_expr="icontains", exclude=True
    )

    clipa = ValueInFilter(field_name="fish__clipa")
    clipa__not = ValueInFilter(field_name="fish__clipa", exclude=True)
    clipa__null = django_filters.BooleanFilter(
        field_name="fish__clipa", lookup_expr="isnull"
    )
    clipa__like = django_filters.CharFilter(
        field_name="fish__clipa", lookup_expr="icontains"
    )
    clipa__not_like = django_filters.CharFilter(
        field_name="fish__clipa", lookup_expr="icontains", exclude=True
    )

    nodc = ValueInFilter(field_name="fish__nodc")
    nodc__not = ValueInFilter(field_name="fish__nodc", exclude=True)
    nodc__null = django_filters.BooleanFilter(
        field_name="fish__nodc", lookup_expr="isnull"
    )
    nodc__like = django_filters.CharFilter(
        field_name="fish__nodc", lookup_expr="icontains"
    )
    nodc__not_like = django_filters.CharFilter(
        field_name="fish__nodc", lookup_expr="icontains", exclude=True
    )

    noda = ValueInFilter(field_name="fish__noda")
    noda__not = ValueInFilter(field_name="fish__noda", exclude=True)
    noda__null = django_filters.BooleanFilter(
        field_name="fish__noda", lookup_expr="isnull"
    )
    noda__like = django_filters.CharFilter(
        field_name="fish__noda", lookup_expr="icontains"
    )
    noda__not_like = django_filters.CharFilter(
        field_name="fish__noda", lookup_expr="icontains", exclude=True
    )
