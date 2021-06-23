import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN127


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

    # fish = slug__in

    preferred = django_filters.BooleanFilter(field_name="preferred")

    agemt__like = ValueInFilter(field_name="agemt", lookup_expr="icontains")
    agemt = ValueInFilter(field_name="agemt")

    xagem__like = ValueInFilter(field_name="xagem", lookup_expr="icontains")
    xagem = ValueInFilter(field_name="xagem")

    edge = ValueInFilter(field_name="edge")

    agea = django_filters.NumberFilter(field_name="agea")
    agea__gte = django_filters.NumberFilter(field_name="agea", lookup_expr="gte")
    agea__lte = django_filters.NumberFilter(field_name="agea", lookup_expr="lte")
    agea__gt = django_filters.NumberFilter(field_name="agea", lookup_expr="gt")
    agea__lt = django_filters.NumberFilter(field_name="agea", lookup_expr="lt")

    nca = django_filters.NumberFilter(field_name="nca")
    nca__gte = django_filters.NumberFilter(field_name="nca", lookup_expr="gte")
    nca__lte = django_filters.NumberFilter(field_name="nca", lookup_expr="lte")
    nca__gt = django_filters.NumberFilter(field_name="nca", lookup_expr="gt")
    nca__lt = django_filters.NumberFilter(field_name="nca", lookup_expr="lt")

    conf = django_filters.NumberFilter(field_name="conf")
    conf__gte = django_filters.NumberFilter(field_name="conf", lookup_expr="gte")
    conf__lte = django_filters.NumberFilter(field_name="conf", lookup_expr="lte")
    conf__gt = django_filters.NumberFilter(field_name="conf", lookup_expr="gt")
    conf__lt = django_filters.NumberFilter(field_name="conf", lookup_expr="lt")

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

    sidep__gte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="fish__catch__effort__sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="fish__catch__effort__sample__grtp")
    gr = ValueInFilter(field_name="fish__catch__effort__sample__gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="fish__catch__effort__sample__grid__grid")

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

    # project attributes
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

    protocol = ValueInFilter(
        field_name="fish__catch__effort__sample__project__protocol__abbrev"
    )

    prj_cd = ValueInFilter(field_name="fish__catch__effort__sample__project__prj_cd")

    prj_cd__like = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__prj_cd",
        lookup_expr="icontains",
    )

    lake = django_filters.CharFilter(
        field_name="fish__catch__effort__sample__project__lake__abbrev",
        lookup_expr="iexact",
    )

    # FISH ATTRIBUTES:
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

    mat = ValueInFilter(field_name="fish__mat")
    mat__null = django_filters.BooleanFilter(
        field_name="fish__mat", lookup_expr="isnull"
    )

    gon = ValueInFilter(field_name="fish__gon")
    gon__null = django_filters.BooleanFilter(
        field_name="fish__gon", lookup_expr="isnull"
    )

    sex = ValueInFilter(field_name="fish__sex")
    sex__null = django_filters.BooleanFilter(
        field_name="fish__sex", lookup_expr="isnull"
    )

    clipc = ValueInFilter(field_name="fish__clipc")
    clipc__null = django_filters.BooleanFilter(
        field_name="fish__clipc", lookup_expr="isnull"
    )

    class Meta:
        model = FN127
        fields = ["conf", "nca", "agea", "edge", "xagem", "agemt", "preferred"]
