import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN125, FN125_Lamprey, FN125Tag


class FN125SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of bio-sample objects by
    by attributes of the biological samples (fn125 data only)"""

    tlen = django_filters.NumberFilter(field_name="tlen")
    tlen__gte = django_filters.NumberFilter(field_name="tlen", lookup_expr="gte")
    tlen__lte = django_filters.NumberFilter(field_name="tlen", lookup_expr="lte")

    flen = django_filters.NumberFilter(field_name="flen")
    flen__gte = django_filters.NumberFilter(field_name="flen", lookup_expr="gte")
    flen__lte = django_filters.NumberFilter(field_name="flen", lookup_expr="lte")

    rwt = django_filters.NumberFilter(field_name="rwt")
    rwt_null = django_filters.BooleanFilter(field_name="rwt", lookup_expr="isnull")
    rwt__gte = django_filters.NumberFilter(field_name="rwt", lookup_expr="gte")
    rwt__lte = django_filters.NumberFilter(field_name="rwt", lookup_expr="lte")

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

    protocol = ValueInFilter(
        field_name="catch__effort__sample__project__protocol__abbrev"
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
        model = FN125Tag
        fields = ["tagstat", "tagid", "tagdoc"]
