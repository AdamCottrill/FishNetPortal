import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN125, FN125_Lamprey, FN125Tag


class FN125SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of bio-sample objects by
    by attributes of the biological samples (fn125 data only)"""

    tlen = django_filters.NumberFilter(field_name="tlen")  # , lookup_expr="exact")
    tlen__gte = django_filters.NumberFilter(field_name="tlen", lookup_expr="gte")
    tlen__lte = django_filters.NumberFilter(field_name="tlen", lookup_expr="lte")
    tlen__gt = django_filters.NumberFilter(field_name="tlen", lookup_expr="gt")
    tlen__lt = django_filters.NumberFilter(field_name="tlen", lookup_expr="lt")

    flen = django_filters.NumberFilter(field_name="flen")
    flen__gte = django_filters.NumberFilter(field_name="flen", lookup_expr="gte")
    flen__lte = django_filters.NumberFilter(field_name="flen", lookup_expr="lte")
    flen__gt = django_filters.NumberFilter(field_name="flen", lookup_expr="gt")
    flen__lt = django_filters.NumberFilter(field_name="flen", lookup_expr="lt")

    rwt = django_filters.NumberFilter(field_name="rwt")
    rwt__null = django_filters.BooleanFilter(field_name="rwt", lookup_expr="isnull")
    rwt__gte = django_filters.NumberFilter(field_name="rwt", lookup_expr="gte")
    rwt__lte = django_filters.NumberFilter(field_name="rwt", lookup_expr="lte")
    rwt__gt = django_filters.NumberFilter(field_name="rwt", lookup_expr="gt")
    rwt__lt = django_filters.NumberFilter(field_name="rwt", lookup_expr="lt")

    mat = ValueInFilter(field_name="mat")
    mat__not = ValueInFilter(field_name="mat", exclude=True)
    mat__null = django_filters.BooleanFilter(field_name="mat", lookup_expr="isnull")

    gon = ValueInFilter(field_name="gon")
    gon__not = ValueInFilter(field_name="gon", exclude=True)
    gon__null = django_filters.BooleanFilter(field_name="gon", lookup_expr="isnull")

    sex = ValueInFilter(field_name="sex")
    sex__not = ValueInFilter(field_name="sex", exclude=True)
    sex__null = django_filters.BooleanFilter(field_name="sex", lookup_expr="isnull")

    clipc = ValueInFilter(field_name="clipc")
    clipc__not = ValueInFilter(field_name="clipc", exclude=True)
    clipc__null = django_filters.BooleanFilter(field_name="clipc", lookup_expr="isnull")

    # girth, agest, fate,
    # these are child tables and might be harder to filter on: age_estimates, lamprey, tags, diet_data

    class Meta:
        model = FN125
        fields = ["sex", "mat", "gon", "tlen", "flen", "rwt", "clipc"]


class FN125Filter(FN125SubFilter):
    """A fitlerset that allows us to select subsets of bio-sample objects
    by attributes of the biological data as well as the parent tables:
    net set, effort, and catch attributes.

    """

    # FN011 ATTRIBUTES

    year = django_filters.CharFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="exact"
    )
    year__gte = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="gt"
    )
    year__lt = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="lt"
    )

    prj_date0 = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date0",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date1",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="catch__effort__sample__project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="catch__effort__sample__project__prj_cd")
    prj_cd__not = ValueInFilter(
        field_name="catch__effort__sample__project__prj_cd", exclude=True
    )

    prj_cd__like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd",
        lookup_expr="endswith",
        exclude=True,
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_nm",
        lookup_expr="icontains",
        exclude=True,
    )

    prj_ldr = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_ldr__username",
        lookup_expr="iexact",
    )

    protocol = ValueInFilter(
        field_name="catch__effort__sample__project__protocol__abbrev"
    )

    protocol__not = ValueInFilter(
        field_name="catch__effort__sample__project__protocol__abbrev", exclude=True
    )

    lake = ValueInFilter(field_name="catch__effort__sample__project__lake__abbrev")

    lake__not = ValueInFilter(
        field_name="catch__effort__sample__project__lake__abbrev", exclude=True
    )

    # FN121 ATTRIBUTES

    sidep__gte = django_filters.NumberFilter(
        field_name="catch__effort__sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="catch__effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="catch__effort__sample__grtp")
    grtp__not = ValueInFilter(field_name="catch__effort__sample__grtp", exclude=True)
    gr = ValueInFilter(field_name="catch__effort__sample__gr")
    gr__not = ValueInFilter(field_name="catch__effort__sample__gr", exclude=True)

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="catch__effort__sample__grid__grid")
    grid__not = NumberInFilter(
        field_name="catch__effort__sample__grid__grid", exclude=True
    )

    effdur__gte = django_filters.NumberFilter(
        field_name="catch__effort__sample__effdur", lookup_expr="gte"
    )
    effdur__lte = django_filters.NumberFilter(
        field_name="catch__effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date__gte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date__lte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date__gte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date__lte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time__gte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time__lte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time__gte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time__lte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # FN122 ATTRIBUTES

    eff = ValueInFilter(field_name="catch__effort__eff")
    eff__not = ValueInFilter(field_name="catch__effort__eff", exclude=True)

    effdst = django_filters.NumberFilter(
        field_name="catch__effort__effdst", lookup_expr="exact"
    )
    effdst__gte = django_filters.NumberFilter(
        field_name="catch__effort__effdst", lookup_expr="gte"
    )
    effdst__lte = django_filters.NumberFilter(
        field_name="catch__effort__effdst", lookup_expr="lte"
    )
    effdst__gt = django_filters.NumberFilter(
        field_name="catch__effort__effdst", lookup_expr="gt"
    )
    effdst__lt = django_filters.NumberFilter(
        field_name="catch__effort__effdst", lookup_expr="lt"
    )

    grdep = django_filters.NumberFilter(
        field_name="catch__effort__grdep", lookup_expr="exact"
    )
    grdep__gte = django_filters.NumberFilter(
        field_name="catch__effort__grdep", lookup_expr="gte"
    )
    grdep__lte = django_filters.NumberFilter(
        field_name="catch__effort__grdep", lookup_expr="lte"
    )
    grdep__gt = django_filters.NumberFilter(
        field_name="catch__effort__grdep", lookup_expr="gt"
    )
    grdep__lt = django_filters.NumberFilter(
        field_name="catch__effort__grdep", lookup_expr="lt"
    )

    grtem0 = django_filters.NumberFilter(
        field_name="catch__effort__grtem0", lookup_expr="exact"
    )
    grtem0__gte = django_filters.NumberFilter(
        field_name="catch__effort__grtem0", lookup_expr="gte"
    )
    grtem0__lte = django_filters.NumberFilter(
        field_name="catch__effort__grtem0", lookup_expr="lte"
    )
    grtem0__gt = django_filters.NumberFilter(
        field_name="catch__effort__grtem0", lookup_expr="gt"
    )
    grtem0__lt = django_filters.NumberFilter(
        field_name="catch__effort__grtem0", lookup_expr="lt"
    )

    grtem1 = django_filters.NumberFilter(
        field_name="catch__effort__grtem1", lookup_expr="exact"
    )
    grtem1__gte = django_filters.NumberFilter(
        field_name="catch__effort__grtem1", lookup_expr="gte"
    )
    grtem1__lte = django_filters.NumberFilter(
        field_name="catch__effort__grtem1", lookup_expr="lte"
    )
    grtem1__gt = django_filters.NumberFilter(
        field_name="catch__effort__grtem1", lookup_expr="gt"
    )
    grtem1__lt = django_filters.NumberFilter(
        field_name="catch__effort__grtem1", lookup_expr="lt"
    )

    # FN123 ATTRIBUTES

    grp = ValueInFilter(field_name="catch__grp")
    grp__not = ValueInFilter(field_name="catch__grp", exclude=True)

    spc = ValueInFilter(field_name="catch__species__spc")
    spc__not = ValueInFilter(field_name="catch__species__spc", exclude=True)

    catcnt = django_filters.NumberFilter(
        field_name="catch__catcnt", lookup_expr="exact"
    )
    catcnt__gte = django_filters.NumberFilter(
        field_name="catch__catcnt", lookup_expr="gte"
    )
    catcnt__lte = django_filters.NumberFilter(
        field_name="catch__catcnt", lookup_expr="lte"
    )
    catcnt__gt = django_filters.NumberFilter(
        field_name="catch__catcnt", lookup_expr="gt"
    )
    catcnt__lt = django_filters.NumberFilter(
        field_name="catch__catcnt", lookup_expr="lt"
    )

    biocnt = django_filters.NumberFilter(
        field_name="catch__biocnt", lookup_expr="exact"
    )
    biocnt__gte = django_filters.NumberFilter(
        field_name="catch__biocnt", lookup_expr="gte"
    )
    biocnt__lte = django_filters.NumberFilter(
        field_name="catch__biocnt", lookup_expr="lte"
    )
    biocnt__gt = django_filters.NumberFilter(
        field_name="catch__biocnt", lookup_expr="gt"
    )
    biocnt__lt = django_filters.NumberFilter(
        field_name="catch__biocnt", lookup_expr="lt"
    )
