import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN122


class FN122InProjectFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of catch count objects by
    by attributes of the catch counts (fn122 data only)"""

    # Effort Attributes
    # we could add gear depth here if it was populated more regularly.
    eff = ValueInFilter(field_name="eff")
    eff_not = ValueInFilter(field_name="eff", exclude=True)

    effdst = django_filters.NumberFilter(field_name="effdst", lookup_expr="exact")
    effdst__gte = django_filters.NumberFilter(field_name="effdst", lookup_expr="gte")
    effdst__lte = django_filters.NumberFilter(field_name="effdst", lookup_expr="lte")
    effdst__gt = django_filters.NumberFilter(field_name="effdst", lookup_expr="gt")
    effdst__lt = django_filters.NumberFilter(field_name="effdst", lookup_expr="lt")

    grdep = django_filters.NumberFilter(field_name="grdep", lookup_expr="exact")
    grdep__gte = django_filters.NumberFilter(field_name="grdep", lookup_expr="gte")
    grdep__lte = django_filters.NumberFilter(field_name="grdep", lookup_expr="lte")
    grdep__gt = django_filters.NumberFilter(field_name="grdep", lookup_expr="gt")
    grdep__lt = django_filters.NumberFilter(field_name="grdep", lookup_expr="lt")

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


class FN122Filter(FN122InProjectFilter):
    """A filter that is inherited from FN122InProjectFilter and allows
    additional filters based on attributes of the parent tables
    (project, net set attributes).
    """

    # net set attributes:

    sidep__gte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="gte"
    )
    sidep__lte = django_filters.NumberFilter(
        field_name="sample__sidep", lookup_expr="lte"
    )

    grtp = ValueInFilter(field_name="sample__grtp")
    grtp__not = ValueInFilter(field_name="sample__grtp", exclude=True)
    gr = ValueInFilter(field_name="sample__gr")
    gr__not = ValueInFilter(field_name="sample__gr", exclude=True)

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

    # project attributes
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

    prj_cd = ValueInFilter(field_name="sample__project__prj_cd")
    prj_cd__not = ValueInFilter(field_name="sample__project__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="sample__project__prj_cd", lookup_expr="icontains", exclude=True
    )

    lake = django_filters.CharFilter(
        field_name="sample__project__lake__abbrev", lookup_expr="iexact"
    )

    lake__not = django_filters.CharFilter(
        field_name="sample__project__lake__abbrev", lookup_expr="iexact", exclude=True
    )

    class Meta:
        model = FN122
        fields = ["eff"]
