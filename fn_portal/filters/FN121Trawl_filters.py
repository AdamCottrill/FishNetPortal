import django_filters

from ..models import FN121Trawl

from .common_filters import NumberInFilter, ValueInFilter

from .FN121AttributeFilter import FN121AttributeFilter


class FN121TrawlFilter(FN121AttributeFilter):
    """A filter that is inherited from FN121AttributeFilter and filter
    by additional trawl attributes

    """

    vessel = ValueInFilter(field_name="vessel__abbrev")
    vessel__not = ValueInFilter(field_name="vessel_abbrev", exclude=True)
    vessel__null = django_filters.BooleanFilter(field_name="vessel__abbrev", lookup_expr="isnull")

    vessel_direction = NumberInFilter(field_name="vessel_direction")
    vessel_direction__not = NumberInFilter(field_name="vessel_abbrev", exclude=True)
    vessel_direction__null = django_filters.BooleanFilter(field_name="vessel_direction", lookup_expr="isnull")

    vessel_speed = django_filters.NumberFilter(field_name="vessel_speed", lookup_expr="exact")
    vessel_speed__gte = django_filters.NumberFilter(field_name="vessel_speed", lookup_expr="gte")
    vessel_speed__lte = django_filters.NumberFilter(field_name="vessel_speed", lookup_expr="lte")
    vessel_speed__gt = django_filters.NumberFilter(field_name="vessel_speed", lookup_expr="gt")
    vessel_speed__lt = django_filters.NumberFilter(field_name="vessel_speed", lookup_expr="lt")
    vessel_speed__null = django_filters.BooleanFilter(
        field_name="vessel_speed", lookup_expr="isnull"
    )
    vessel_speed__not_null = django_filters.BooleanFilter(
        field_name="vessel_speed", lookup_expr="isnull", exclude=True
    )

    warp = django_filters.NumberFilter(field_name="warp", lookup_expr="exact")
    warp__gte = django_filters.NumberFilter(field_name="warp", lookup_expr="gte")
    warp__lte = django_filters.NumberFilter(field_name="warp", lookup_expr="lte")
    warp__gt = django_filters.NumberFilter(field_name="warp", lookup_expr="gt")
    warp__lt = django_filters.NumberFilter(field_name="warp", lookup_expr="lt")
    warp__null = django_filters.BooleanFilter(
        field_name="warp", lookup_expr="isnull"
    )
    warp__not_null = django_filters.BooleanFilter(
        field_name="warp", lookup_expr="isnull", exclude=True
    )


    class Meta:
        model = FN121Trawl
        fields = [
            "vessel",
            "vessel_speed",
            "vessel_direction",
            "warp",
        ]
