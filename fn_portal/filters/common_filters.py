import django_filters

from common.models import Species


class ValueInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class SpeciesFilter(django_filters.FilterSet):

    spc = ValueInFilter(field_name="spc")

    spc_nmco_like = django_filters.CharFilter(
        field_name="spc_nmco", lookup_expr="icontains"
    )

    spc_nmsc_like = django_filters.CharFilter(
        field_name="spc_nmsc", lookup_expr="icontains"
    )

    class Meta:
        model = Species
        fields = ["spc", "spc_nmco", "spc_nmsc"]
