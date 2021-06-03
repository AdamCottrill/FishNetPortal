"""Django-filter classes that will be used to filter stocking objects.
The will be used in both views and api serializers.

"""

import django_filters

from .models import (
    FN011,
    FN121,
    FN122,
    FN123,
    FN125,
    FN125_Lamprey,
    FN125Tag,
    FN126,
    FN127,
)
from common.models import Species


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class SpeciesFilter(django_filters.FilterSet):

    spc = ValueInFilter(field_name="spc")

    spc_nmco_like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains"
    )

    spc_nmsc_like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains"
    )

    class Meta:
        model = Species
        fields = ["spc", "spc_nmco", "spc_nmsc"]


class FN011Filter(django_filters.FilterSet):

    # need to add:
    # protocol
    # management area
    # Region of interest.
    # within km of point proximity=0.5;POINT(45.5 -81.1)

    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")

    start_date = django_filters.DateFilter(
        field_name="prj_date0", help_text="format: yyyy-mm-dd"
    )
    start_date_gte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    start_date_lte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    end_date = django_filters.DateFilter(
        field_name="prj_date1", help_text="format: yyyy-mm-dd"
    )
    end_date_gte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    end_date_lte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    prj_cd = django_filters.CharFilter(lookup_expr="icontains")

    prj_cd_in = ValueInFilter(field_name="prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains"
    )

    prj_nm_like = django_filters.CharFilter(
        field_name="prj_nm", lookup_expr="icontains"
    )

    lake = django_filters.CharFilter(field_name="lake__abbrev", lookup_expr="iexact")
    prj_ldr = django_filters.CharFilter(
        field_name="prj_ldr__username", lookup_expr="iexact"
    )
    suffix = django_filters.CharFilter(field_name="prj_cd", lookup_expr="endswith")

    spc_caught = ValueInFilter(field_name="samples__effort__catch__species__spc")

    # spc_caught
    # spc_sampled
    # gr
    # grtp

    # source = ValueInFilter(field_name="source", lookup_expr="iexact")

    class Meta:
        model = FN011
        fields = [
            "year",
            "prj_cd",
            "prj_nm",
            "prj_ldr",
            "prj_date0",
            "prj_date1",
            "lake",
            "source",
        ]


class FN121SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    net set attributes."""

    active = django_filters.BooleanFilter(field_name="effdt1", lookup_expr="isnull")

    sidep_gte = django_filters.NumberFilter(field_name="sidep", lookup_expr="gte")
    sidep_lte = django_filters.NumberFilter(field_name="sidep", lookup_expr="lte")

    grtp = ValueInFilter(field_name="grtp")
    gr = ValueInFilter(field_name="gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="grid__grid")

    effdur_gte = django_filters.NumberFilter(field_name="effdur", lookup_expr="gte")
    effdur_lte = django_filters.NumberFilter(field_name="effdur", lookup_expr="lte")

    set_date = django_filters.DateFilter(
        field_name="effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date_gte = django_filters.DateFilter(
        field_name="effdt0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    set_date_lte = django_filters.DateFilter(
        field_name="effdt0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    lift_date = django_filters.DateFilter(
        field_name="effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date_gte = django_filters.DateFilter(
        field_name="effdt1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    lift_date_lte = django_filters.DateFilter(
        field_name="effdt1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    set_time = django_filters.TimeFilter(field_name="efftm0", help_text="format: HH:MM")
    set_time_gte = django_filters.TimeFilter(
        field_name="efftm0", lookup_expr="gte", help_text="format: HH:MM"
    )
    set_time_lte = django_filters.TimeFilter(
        field_name="efftm0", lookup_expr="lte", help_text="format: HH:MM"
    )

    lift_time = django_filters.TimeFilter(
        field_name="efftm1", help_text="format: HH:MM"
    )
    lift_time_gte = django_filters.TimeFilter(
        field_name="efftm1", lookup_expr="gte", help_text="format: HH:MM"
    )
    lift_time_lte = django_filters.TimeFilter(
        field_name="efftm1", lookup_expr="lte", help_text="format: HH:MM"
    )

    # active (effdt1 is null)
    # effst
    # orient?
    # roi

    class Meta:
        model = FN121
        fields = [
            "project__year",
            "project__prj_cd",
            "project__lake",
            "project__source",
            "grid__grid",
            "sidep",
            "gr",
            "grtp",
        ]


class FN121Filter(FN121SubFilter):
    """Extends the FN121SubFilter to include additional fields that
    are assoicated with parent objects.
    """

    year = django_filters.CharFilter(field_name="project__year", lookup_expr="exact")
    first_year = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )

    prj_cd = django_filters.CharFilter(field_name="project__prj_cd")

    prj_cd_in = ValueInFilter(field_name="project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )

    lake = django_filters.CharFilter(
        field_name="project__lake__abbrev", lookup_expr="iexact"
    )

    class Meta:
        model = FN121
        fields = [
            "project__year",
            "project__prj_cd",
            "project__lake",
            "project__source",
            "grid__grid",
            "sidep",
            "gr",
            "grtp",
        ]


class FN122SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn122 data only)"""

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="eff")

    class Meta:
        model = FN122
        fields = ["eff"]


class FN122Filter(FN122SubFilter):
    """A filter that is inherited from FN122SubFilter and allows
    additional filters based on attributes of the parent tables
    (project, net set attributes).

    """

    # net set attributes:

    sidep_gte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="gte"
    )
    sidep_lte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="sample__grtp")
    gr = ValueInFilter(field_name="sample__gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="sample__grid__grid")

    effdur_gte = django_filters.NumberFilter(
        field_name="sample__effdur", lookup_expr="gte"
    )
    effdur_lte = django_filters.NumberFilter(
        field_name="sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date_gte = django_filters.DateFilter(
        field_name="sample__effdt0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    set_date_lte = django_filters.DateFilter(
        field_name="sample__effdt0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    lift_date = django_filters.DateFilter(
        field_name="sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date_gte = django_filters.DateFilter(
        field_name="sample__effdt1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    lift_date_lte = django_filters.DateFilter(
        field_name="sample__effdt1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    set_time = django_filters.TimeFilter(
        field_name="sample__efftm0", help_text="format: HH:MM"
    )
    set_time_gte = django_filters.TimeFilter(
        field_name="sample__efftm0", lookup_expr="gte", help_text="format: HH:MM"
    )
    set_time_lte = django_filters.TimeFilter(
        field_name="sample__efftm0", lookup_expr="lte", help_text="format: HH:MM"
    )

    lift_time = django_filters.TimeFilter(
        field_name="sample__efftm1", help_text="format: HH:MM"
    )
    lift_time_gte = django_filters.TimeFilter(
        field_name="sample__efftm1", lookup_expr="gte", help_text="format: HH:MM"
    )
    lift_time_lte = django_filters.TimeFilter(
        field_name="sample__efftm1", lookup_expr="lte", help_text="format: HH:MM"
    )

    # project attributes
    year = django_filters.CharFilter(
        field_name="sample__project__year", lookup_expr="exact"
    )
    first_year = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="sample__project__year", lookup_expr="lte"
    )

    prj_cd = django_filters.CharFilter(field_name="sample__project__prj_cd")

    prj_cd_in = ValueInFilter(field_name="sample__project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="icontains"
    )

    lake = django_filters.CharFilter(
        field_name="sample__project__lake__abbrev", lookup_expr="iexact"
    )

    class Meta:
        model = FN122
        fields = ["eff"]


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


class FN125SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of bio-sample objects by
    by attributes of the biological samples (fn125 data only)"""

    tlen = django_filters.NumberFilter(field_name="tlen")
    tlen_gte = django_filters.NumberFilter(field_name="tlen", lookup_expr="gte")
    tlen_lte = django_filters.NumberFilter(field_name="tlen", lookup_expr="lte")

    flen = django_filters.NumberFilter(field_name="flen")
    flen_gte = django_filters.NumberFilter(field_name="flen", lookup_expr="gte")
    flen_lte = django_filters.NumberFilter(field_name="flen", lookup_expr="lte")

    rwt = django_filters.NumberFilter(field_name="rwt")
    rwt_null = django_filters.BooleanFilter(field_name="rwt", lookup_expr="isnull")
    rwt_gte = django_filters.NumberFilter(field_name="rwt", lookup_expr="gte")
    rwt_lte = django_filters.NumberFilter(field_name="rwt", lookup_expr="lte")

    mat = ValueInFilter(field_name="mat")
    gon = ValueInFilter(field_name="gon")
    sex = ValueInFilter(field_name="sex")
    clipc = ValueInFilter(field_name="clipc")

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

    # catch attributes:
    grp = ValueInFilter(field_name="catch__grp")
    spc = ValueInFilter(field_name="catch__species__spc")

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="catch__effort__eff")

    # net set attributes:

    sidep_gte = django_filters.NumberFilter(
        field_name="catch__effort__sample__sidep", lookup_expr="gte"
    )
    sidep_lte = django_filters.NumberFilter(
        field_name="catch__effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="catch__effort__sample__grtp")
    gr = ValueInFilter(field_name="catch__effort__sample__gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="catch__effort__sample__grid__grid")

    effdur_gte = django_filters.NumberFilter(
        field_name="catch__effort__sample__effdur", lookup_expr="gte"
    )
    effdur_lte = django_filters.NumberFilter(
        field_name="catch__effort__sample__effdur", lookup_expr="lte"
    )

    set_date = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date_gte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    set_date_lte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    lift_date = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date_gte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    lift_date_lte = django_filters.DateFilter(
        field_name="catch__effort__sample__effdt1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    set_time = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0", help_text="format: HH:MM"
    )
    set_time_gte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    set_time_lte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm0",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    lift_time = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1", help_text="format: HH:MM"
    )
    lift_time_gte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1",
        lookup_expr="gte",
        help_text="format: HH:MM",
    )
    lift_time_lte = django_filters.TimeFilter(
        field_name="catch__effort__sample__efftm1",
        lookup_expr="lte",
        help_text="format: HH:MM",
    )

    # project attributes
    year = django_filters.CharFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="exact"
    )
    first_year = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="gte"
    )
    last_year = django_filters.NumberFilter(
        field_name="catch__effort__sample__project__year", lookup_expr="lte"
    )

    prj_cd = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd"
    )

    prj_cd_in = ValueInFilter(field_name="catch__effort__sample__project__prj_cd")

    prj_cd_like = django_filters.CharFilter(
        field_name="catch__effort__sample__project__prj_cd", lookup_expr="icontains"
    )

    lake = django_filters.CharFilter(
        field_name="catch__effort__sample__project__lake__abbrev", lookup_expr="iexact"
    )

    tlen = django_filters.NumberFilter(field_name="fish__tlen")
    tlen_gte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="gte")
    tlen_lte = django_filters.NumberFilter(field_name="fish__tlen", lookup_expr="lte")

    flen = django_filters.NumberFilter(field_name="fish__flen")
    flen_gte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="gte")
    flen_lte = django_filters.NumberFilter(field_name="fish__flen", lookup_expr="lte")

    rwt = django_filters.NumberFilter(field_name="fish__rwt")
    rwt_null = django_filters.BooleanFilter(
        field_name="fish__rwt", lookup_expr="isnull"
    )
    rwt_gte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="gte")
    rwt_lte = django_filters.NumberFilter(field_name="fish__rwt", lookup_expr="lte")

    mat = ValueInFilter(field_name="fish__mat")
    gon = ValueInFilter(field_name="fish__gon")
    sex = ValueInFilter(field_name="fish__sex")
    clipc = ValueInFilter(field_name="fish__clipc")

    class Meta:
        model = FN125
        fields = ["sex", "mat", "gon", "tlen", "flen", "rwt", "clipc"]


class FN125LampreySubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of lamprey records by
    by attributes of the the lamprey wounds (fn125Lam data only)"""

    lamijc_size = django_filters.NumberFilter(field_name="lamijc_size")
    lamijc_size_gte = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="gte"
    )
    lamijc_size_lte = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="lte"
    )
    lamijc_size_gt = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="gt"
    )
    lamijc_size_lt = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="lt"
    )

    xlam = ValueInFilter(field_name="xlam")
    lamijc = ValueInFilter(field_name="lamijc")
    lamijc_type = ValueInFilter(field_name="lamijc_type")

    class Meta:
        model = FN125_Lamprey
        fields = ["xlam", "lamijc", "lamijc_type", "lamijc_size"]


class FN125LampreyFilter(FN125LampreySubFilter):
    """A fitlerset that allows us to select subsets of lamprey wound records
    by attributes of the wound as well as the parent tables:
    net set, effort, and catch attributes.

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
        model = FN125_Lamprey
        fields = ["xlam", "lamijc", "lamijc_type", "lamijc_size"]


class FN125TagSubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of tag objects by
    by attributes of the tag (fn125 tag data only)"""

    tagid_like = ValueInFilter(field_name="tagid", lookup_expr="icontains")
    tagdoc_like = ValueInFilter(field_name="tagdoc", lookup_expr="icontains")

    tagstat = ValueInFilter(field_name="tagstat")
    tagid = ValueInFilter(field_name="tagid")
    tagdoc = ValueInFilter(field_name="tagdoc")

    # consider splitting up tagdoc into consitiuent fields to make it
    # easier to filter by colour, placement tag type and agency.

    class Meta:
        model = FN125Tag
        fields = ["tagstat", "tagid", "tagdoc"]


class FN125TagFilter(FN125TagSubFilter):
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
        model = FN125Tag
        fields = ["tagstat", "tagid", "tagdoc"]


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


class FN127SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of FN127 table (age estimates/interpretations) by
    by attributes of the age estimates (FN127 data only)"""

    # preferred = True/False
    # agemt - in, like
    # xagem in and like
    # conf =, gte, lte, gt, lt
    # nca =, gte, lte, gt, lt
    # agea =, gte, lte, gt, lt
    # edge in

    # fish = slug_in

    preferred = django_filters.BooleanFilter(field_name="preferred")

    agemt_like = ValueInFilter(field_name="agemt", lookup_expr="icontains")
    agemt = ValueInFilter(field_name="agemt")

    xagem_like = ValueInFilter(field_name="xagem", lookup_expr="icontains")
    xagem = ValueInFilter(field_name="xagem")

    edge = ValueInFilter(field_name="edge")

    agea = django_filters.NumberFilter(field_name="agea")
    agea_gte = django_filters.NumberFilter(field_name="agea", lookup_expr="gte")
    agea_lte = django_filters.NumberFilter(field_name="agea", lookup_expr="lte")
    agea_gt = django_filters.NumberFilter(field_name="agea", lookup_expr="gt")
    agea_lt = django_filters.NumberFilter(field_name="agea", lookup_expr="lt")

    nca = django_filters.NumberFilter(field_name="nca")
    nca_gte = django_filters.NumberFilter(field_name="nca", lookup_expr="gte")
    nca_lte = django_filters.NumberFilter(field_name="nca", lookup_expr="lte")
    nca_gt = django_filters.NumberFilter(field_name="nca", lookup_expr="gt")
    nca_lt = django_filters.NumberFilter(field_name="nca", lookup_expr="lt")

    conf = django_filters.NumberFilter(field_name="conf")
    conf_gte = django_filters.NumberFilter(field_name="conf", lookup_expr="gte")
    conf_lte = django_filters.NumberFilter(field_name="conf", lookup_expr="lte")
    conf_gt = django_filters.NumberFilter(field_name="conf", lookup_expr="gt")
    conf_lt = django_filters.NumberFilter(field_name="conf", lookup_expr="lt")

    class Meta:
        model = FN127
        fields = ["conf", "nca", "agea", "edge", "xagem", "agemt", "preferred"]


class FN127Filter(FN127SubFilter):
    """A fitlerset that allows us to select subsets of age estimate objects
    by attributes of the age estimate as well as the parent tables:
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
        model = FN127
        fields = ["conf", "nca", "agea", "edge", "xagem", "agemt", "preferred"]
