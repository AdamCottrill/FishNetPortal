"""Django-filter classes that will be used to filter stocking objects.
The will be used in both views and api serializers.

"""

import django_filters

from .models import FN011


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class FN011Filter(django_filters.FilterSet):

    # need to add:
    # protocol
    # management area
    #

    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")
    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    prj_cd = django_filters.CharFilter(lookup_expr="icontains")

    lake = django_filters.CharFilter(field_name="lake__abbrev", lookup_expr="exact")
    prj_ldr = django_filters.CharFilter(
        field_name="prj_ldr__username", lookup_expr="iexact"
    )
    suffix = django_filters.CharFilter(field_name="prj_cd", lookup_expr="endswith")

    # source = ValueInFilter(field_name="project_type__source", lookup_expr="in")

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
        ]
