import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN125_Lamprey

from .FishAttr_filters import FishAttrFilters


class FN125LampreyFilter(FishAttrFilters):
    """A filter set class for lamprey data. Inherits all of the filters in
    FishAttrs and add some that are specific to Lamprey attributes.
    """

    lamijc_size = django_filters.NumberFilter(field_name="lamijc_size")
    lamijc_size__gte = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="gte"
    )
    lamijc_size__lte = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="lte"
    )
    lamijc_size__gt = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="gt"
    )
    lamijc_size__lt = django_filters.NumberFilter(
        field_name="lamijc_size", lookup_expr="lt"
    )

    xlam = ValueInFilter(field_name="xlam")
    xlam__not = ValueInFilter(field_name="xlam", exclude=True)
    xlam__null = django_filters.BooleanFilter(field_name="xlam", lookup_expr="isnull")

    lamijc_type = ValueInFilter(field_name="lamijc_type")
    lamijc_type__not = ValueInFilter(field_name="lamijc_type", exclude=True)
    lamijc_type__null = django_filters.BooleanFilter(
        field_name="lamijc_type", lookup_expr="isnull"
    )

    class Meta:
        model = FN125_Lamprey
        fields = ["xlam", "lamijc_type", "lamijc_size"]
