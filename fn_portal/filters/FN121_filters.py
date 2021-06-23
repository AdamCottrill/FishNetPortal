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
    gr = ValueInFilter(field_name="gr")

    # grid is a little trick - requires us to filter lake too - user beware!
    grid = NumberInFilter(field_name="grid__grid")

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
    are assoicated with parent objects.
    """

    year = django_filters.CharFilter(field_name="project__year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(field_name="project__year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="project__year", lookup_expr="lt")

    protocol = ValueInFilter(field_name="project__protocol__abbrev")

    prj_cd = ValueInFilter(field_name="project__prj_cd")

    prj_cd__like = django_filters.CharFilter(
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
