"""Django-filter classes that will be used to filter stocking objects.
The will be used in both views and api serializers.

"""

import django_filters

from .models import FN011, FN121, FN122, FN123, FN125


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class FN011Filter(django_filters.FilterSet):

    # need to add:
    # protocol
    # management area
    # Region of interest.

    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    prj_cd = django_filters.CharFilter(lookup_expr="icontains")

    lake = django_filters.CharFilter(field_name="lake__abbrev", lookup_expr="iexact")
    prj_ldr = django_filters.CharFilter(
        field_name="prj_ldr__username", lookup_expr="iexact"
    )
    suffix = django_filters.CharFilter(field_name="prj_cd", lookup_expr="endswith")

    # source = ValueInFilter(field_name="source", lookup_expr="iexact")

    class Meta:
        model = FN011
        fields = [
            "year",
            "prj_cd",
            # "prj_nm",
            "prj_ldr",
            # "prj_date0",
            # "prj_date1",
            "lake",
            "source",
        ]


class FN121InProjectFilter(django_filters.FilterSet):
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


class FN121Filter(FN121InProjectFilter):
    """Extends the FN121InProjectFilter to include additional fields that
    are assoicated with parent objects. There is no point in filtering
    net sets by year when they are all from the same project - by
    definintion, they are all from the same year anyway.

    inheriting from an existing filterset keeps the documentation
    cleaner as it does not include filters that wouldn't really apply
    to some endpoints.

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


class FN122InProjectFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn122 data only)"""

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="eff")

    class Meta:
        model = FN122
        fields = ["eff"]


class FN122Filter(FN122InProjectFilter):
    """A filter that is inherited from FN122InProjectFilter and allows
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


class FN123InProjectFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn123 data only)"""

    grp = ValueInFilter(field_name="grp")
    spc = ValueInFilter(field_name="species__spc")

    class Meta:
        model = FN123
        fields = ["species__spc", "grp"]


class FN123Filter(FN123InProjectFilter):
    """A filter that is inherited from FN123InProjectFilter and allows
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


class FN125InProjectFilter(django_filters.FilterSet):
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


class FN125Filter(FN125InProjectFilter):
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

    class Meta:
        model = FN125
        fields = ["sex", "mat", "gon", "tlen", "flen", "rwt", "clipc"]
