import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN121


class FN121SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    net set attributes."""

    active = django_filters.BooleanFilter(field_name="effdt1", lookup_expr="isnull")

    sidep__gte = django_filters.NumberFilter(field_name="sidep", lookup_expr="gte")
    sidep__lte = django_filters.NumberFilter(field_name="sidep", lookup_expr="lte")

    grtp = ValueInFilter(field_name="grtp")
    grtp__not = ValueInFilter(field_name="grtp", exclude=True)

    gr = ValueInFilter(field_name="gr")
    gr__not = ValueInFilter(field_name="gr", exclude=True)

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="grid__grid")
    grid__not = NumberInFilter(field_name="grid__grid", exclude=True)

    effdur__gte = django_filters.NumberFilter(field_name="effdur", lookup_expr="gte")
    effdur__lte = django_filters.NumberFilter(field_name="effdur", lookup_expr="lte")

    set_date = django_filters.DateFilter(
        field_name="effdt0", help_text="format: yyyy-mm-dd"
    )
    set_date__gte = django_filters.DateFilter(
        field_name="effdt0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    set_date__lte = django_filters.DateFilter(
        field_name="effdt0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    lift_date = django_filters.DateFilter(
        field_name="effdt1", help_text="format: yyyy-mm-dd"
    )
    lift_date__gte = django_filters.DateFilter(
        field_name="effdt1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    lift_date__lte = django_filters.DateFilter(
        field_name="effdt1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    set_time = django_filters.TimeFilter(field_name="efftm0", help_text="format: HH:MM")
    set_time__gte = django_filters.TimeFilter(
        field_name="efftm0", lookup_expr="gte", help_text="format: HH:MM"
    )
    set_time__lte = django_filters.TimeFilter(
        field_name="efftm0", lookup_expr="lte", help_text="format: HH:MM"
    )

    lift_time = django_filters.TimeFilter(
        field_name="efftm1", help_text="format: HH:MM"
    )
    lift_time__gte = django_filters.TimeFilter(
        field_name="efftm1", lookup_expr="gte", help_text="format: HH:MM"
    )
    lift_time__lte = django_filters.TimeFilter(
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
    are associated with parent objects.
    """

    # FN011 ATTRIBUTES
    year = django_filters.CharFilter(field_name="project__year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(field_name="project__year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="project__year", lookup_expr="lt")

    prj_date0 = django_filters.DateFilter(
        field_name="project__prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="project__prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    protocol = ValueInFilter(field_name="project__protocol__abbrev")
    protocol__not = ValueInFilter(field_name="project__protocol__abbrev", exclude=True)

    prj_cd = ValueInFilter(field_name="project__prj_cd")
    prj_cd__not = ValueInFilter(field_name="project__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains", exclude=True
    )

    prj_ldr = django_filters.CharFilter(
        field_name="project__prj_ldr__username", lookup_expr="iexact"
    )

    lake = ValueInFilter(field_name="project__lake__abbrev")

    lake__not = ValueInFilter(field_name="project__lake__abbrev", exclude=True)

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
