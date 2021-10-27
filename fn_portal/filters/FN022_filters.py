import django_filters

from ..models import FN022
from .common_filters import NumberInFilter, ValueInFilter


class FN022SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    net set attributes."""

    ssn_date0 = django_filters.DateFilter(
        field_name="ssn_date0", help_text="format: yyyy-mm-dd"
    )
    ssn_date0__gte = django_filters.DateFilter(
        field_name="ssn_date0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    ssn_date0__lte = django_filters.DateFilter(
        field_name="ssn_date0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    ssn_date1 = django_filters.DateFilter(
        field_name="ssn_date1", help_text="format: yyyy-mm-dd"
    )
    ssn_date1__gte = django_filters.DateFilter(
        field_name="ssn_date1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    ssn_date1__lte = django_filters.DateFilter(
        field_name="ssn_date1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    ssn = ValueInFilter(field_name="ssn")
    ssn__not = ValueInFilter(field_name="ssn", exclude=True)

    ssn__like = django_filters.CharFilter(field_name="ssn", lookup_expr="icontains")

    ssn__not_like = django_filters.CharFilter(
        field_name="ssn", lookup_expr="icontains", exclude=True
    )

    ssn_des = ValueInFilter(field_name="ssn_des")
    ssn_des__not = ValueInFilter(field_name="ssn_des", exclude=True)

    ssn_des__like = django_filters.CharFilter(
        field_name="ssn_des", lookup_expr="icontains"
    )

    ssn_des__not_like = django_filters.CharFilter(
        field_name="ssn_des", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = FN022
        fields = ["ssn", "ssn_des", "ssn_date0", "ssn_date1"]


class FN022Filter(FN022SubFilter):
    """Extends the FN022SubFilter to include additional fields that
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

    protocol = ValueInFilter(field_name="project__protocol__abbrev")
    protocol__not = ValueInFilter(field_name="project__protocol__abbrev", exclude=True)

    lake = ValueInFilter(field_name="project__lake__abbrev")

    lake__not = ValueInFilter(field_name="project__lake__abbrev", exclude=True)

    class Meta:
        model = FN022
        fields = [
            "project__year",
            "project__prj_cd",
            "project__lake",
            "project__source",
            "ssn",
            "ssn_des",
            "ssn_date0",
            "ssn_date1",
        ]
