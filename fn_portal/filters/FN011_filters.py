import django_filters

from .common_filters import ValueInFilter

from ..models import (
    FN011,
)


class FN011Filter(django_filters.FilterSet):

    # need to add:
    # protocol
    # management area
    # Region of interest.
    # within km of point proximity=0.5;POINT(45.5 -81.1)

    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    year__lte = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    year__gt = django_filters.NumberFilter(field_name="year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="year", lookup_expr="lt")

    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")

    start_date = django_filters.DateFilter(
        field_name="prj_date0", help_text="format: yyyy-mm-dd"
    )
    start_date__gte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    start_date__lte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    end_date = django_filters.DateFilter(
        field_name="prj_date1", help_text="format: yyyy-mm-dd"
    )
    end_date__gte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    end_date__lte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    protocol = ValueInFilter(field_name="protocol__abbrev")

    prj_cd = ValueInFilter(field_name="prj_cd")

    prj_cd__like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains"
    )

    prj_nm__like = django_filters.CharFilter(
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
