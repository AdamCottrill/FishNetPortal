"""Django-filter classes that will be used to filter stocking objects.
The will be used in both views and api serializers.

"""

import django_filters

from fn_portal.models import FN011


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class FN011Filter(django_filters.FilterSet):

    # need to add:
    # protocol
    # management area
    #

    first_year = django_filters.NumberFilter(field_name="year", lookup_expr="gte")
    last_year = django_filters.NumberFilter(field_name="year", lookup_expr="lte")
    year = django_filters.CharFilter(field_name="year", lookup_expr="exact")

    # lake = ValueInFilter(field_name="jurisdiction__lake__abbrev", lookup_expr="in")
    lake = django_filters.CharFilter(field_name="lake", lookup_expr="exact")
    lead = django_filters.CharFilter(field_name="prj_ldr", lookup_expr="exact")
    suffix = django_filters.CharFilter(field_name="prj_cd", lookup_expr="endswith")

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
