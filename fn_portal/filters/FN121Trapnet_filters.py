import django_filters

from ..models import FN121Trapnet

from .common_filters import ValueInFilter

from .FN121AttributeFilter import FN121AttributeFilter


class FN121TrapnetFilter(FN121AttributeFilter):
    """A filter that is inherited from FN121AttributeFilter and filter
    by additional trapnet attributes

    """

    bottom_type = ValueInFilter(field_name="bottom__abbrev")
    bottom_type__not = ValueInFilter(field_name="bottom__abbrev", exclude=True)
    bottom_type__null = django_filters.BooleanFilter(
        field_name="bottom__abbrev", lookup_expr="isnull"
    )

    cover_type = ValueInFilter(field_name="cover__abbrev")
    cover_type__not = ValueInFilter(field_name="cover__abbrev", exclude=True)
    cover_type__null = django_filters.BooleanFilter(
        field_name="cover__abbrev", lookup_expr="isnull"
    )

    vegetation = django_filters.NumberFilter(
        field_name="vegetation", lookup_expr="exact"
    )
    vegetation__gte = django_filters.NumberFilter(
        field_name="vegetation", lookup_expr="gte"
    )
    vegetation__lte = django_filters.NumberFilter(
        field_name="vegetation", lookup_expr="lte"
    )
    vegetation__gt = django_filters.NumberFilter(
        field_name="vegetation", lookup_expr="gt"
    )
    vegetation__lt = django_filters.NumberFilter(
        field_name="vegetation", lookup_expr="lt"
    )
    vegetation__null = django_filters.BooleanFilter(
        field_name="vegetation", lookup_expr="isnull"
    )
    vegetation__not_null = django_filters.BooleanFilter(
        field_name="vegetation", lookup_expr="isnull", exclude=True
    )

    lead_angle = django_filters.NumberFilter(
        field_name="lead_angle", lookup_expr="exact"
    )
    lead_angle__gte = django_filters.NumberFilter(
        field_name="lead_angle", lookup_expr="gte"
    )
    lead_angle__lte = django_filters.NumberFilter(
        field_name="lead_angle", lookup_expr="lte"
    )
    lead_angle__gt = django_filters.NumberFilter(
        field_name="lead_angle", lookup_expr="gt"
    )
    lead_angle__lt = django_filters.NumberFilter(
        field_name="lead_angle", lookup_expr="lt"
    )
    lead_angle__null = django_filters.BooleanFilter(
        field_name="lead_angle", lookup_expr="isnull"
    )
    lead_angle__not_null = django_filters.BooleanFilter(
        field_name="lead_angle", lookup_expr="isnull", exclude=True
    )

    leaduse = django_filters.NumberFilter(field_name="leaduse", lookup_expr="exact")
    leaduse__gte = django_filters.NumberFilter(field_name="leaduse", lookup_expr="gte")
    leaduse__lte = django_filters.NumberFilter(field_name="leaduse", lookup_expr="lte")
    leaduse__gt = django_filters.NumberFilter(field_name="leaduse", lookup_expr="gt")
    leaduse__lt = django_filters.NumberFilter(field_name="leaduse", lookup_expr="lt")
    leaduse__null = django_filters.BooleanFilter(
        field_name="leaduse", lookup_expr="isnull"
    )
    leaduse__not_null = django_filters.BooleanFilter(
        field_name="leaduse", lookup_expr="isnull", exclude=True
    )

    distoff = django_filters.NumberFilter(field_name="distoff", lookup_expr="exact")
    distoff__gte = django_filters.NumberFilter(field_name="distoff", lookup_expr="gte")
    distoff__lte = django_filters.NumberFilter(field_name="distoff", lookup_expr="lte")
    distoff__gt = django_filters.NumberFilter(field_name="distoff", lookup_expr="gt")
    distoff__lt = django_filters.NumberFilter(field_name="distoff", lookup_expr="lt")
    distoff__null = django_filters.BooleanFilter(
        field_name="distoff", lookup_expr="isnull"
    )
    distoff__not_null = django_filters.BooleanFilter(
        field_name="distoff", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = FN121Trapnet
        fields = [
            "bottom_type",
            "cover_type",
            "vegetation",
            "lead_angle",
            "leaduse",
            "distoff",
        ]
