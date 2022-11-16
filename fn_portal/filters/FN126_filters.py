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

    lifestage_like = ValueInFilter(field_name="lifestage", lookup_expr="icontains")
    lifestage = ValueInFilter(field_name="lifestage")
    lifestage__not = ValueInFilter(field_name="lifestage", exclude=True)

    fdcnt = django_filters.NumberFilter(field_name="fdcnt")
    fdcnt__gte = django_filters.NumberFilter(field_name="fdcnt", lookup_expr="gte")
    fdcnt__lte = django_filters.NumberFilter(field_name="fdcnt", lookup_expr="lte")
    fdcnt__gt = django_filters.NumberFilter(field_name="fdcnt", lookup_expr="gt")
    fdcnt__lt = django_filters.NumberFilter(field_name="fdcnt", lookup_expr="lt")

    class Meta:
        model = FN126
        fields = ["taxon", "fdcnt"]
