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

    # duplicated here - for the html front end filters:
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")

    prj_date0 = django_filters.DateFilter(
        field_name="prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="prj_date0", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    prj_date1 = django_filters.DateFilter(
        field_name="prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="gte", help_text="format: yyyy-mm-dd"
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="prj_date1", lookup_expr="lte", help_text="format: yyyy-mm-dd"
    )

    protocol = ValueInFilter(field_name="protocol__abbrev")
    protocol__not = ValueInFilter(field_name="protocol__abbrev", exclude=True)

    prj_cd = ValueInFilter(field_name="prj_cd")
    prj_cd__not = ValueInFilter(field_name="prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains"
    )
    prj_cd__not_like = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="prj_nm", lookup_expr="icontains", exclude=True
    )

    prj_ldr = django_filters.CharFilter(
        field_name="prj_ldr__username", lookup_expr="iexact"
    )

    lake = ValueInFilter(field_name="lake__abbrev")
    lake__not = ValueInFilter(field_name="lake__abbrev", exclude=True)

    spc_caught = ValueInFilter(field_name="samples__effort__catch__species__spc")

    status = ValueInFilter(field_name="status")
    status__not = ValueInFilter(field_name="status", exclude=True)

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
            "status",
        ]
