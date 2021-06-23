import django_filters

from .common_filters import ValueInFilter, NumberInFilter
from ..models import FN126

from .FishAttr_filters import FishAttrFilters


class FN126Filter(FishAttrFilters):
    """A fitlerset that allows us to select subsets of FN126 table (diet data) by
    by attributes of the diet items (fn126 data only)"""

    taxon_like = ValueInFilter(field_name="taxon", lookup_expr="icontains")
    taxon = ValueInFilter(field_name="taxon")
    taxon__not = ValueInFilter(field_name="taxon", exclude=True)

    foodcnt = django_filters.NumberFilter(field_name="foodcnt")
    foodcnt__gte = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="gte")
    foodcnt__lte = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="lte")
    foodcnt__gt = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="gt")
    foodcnt__lt = django_filters.NumberFilter(field_name="foodcnt", lookup_expr="lt")

    class Meta:
        model = FN126
        fields = ["taxon", "foodcnt"]
