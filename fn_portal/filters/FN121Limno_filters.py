import django_filters

from ..models import FN121Limno

from .FN121AttributeFilter import FN121AttributeFilter


class FN121LimnoFilter(FN121AttributeFilter):
    """A filter that is inherited from FN121AttributeFilter and filter
    by additional Limnological attributes

    """

    o2gear0 = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="exact")
    o2gear0__gte = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="gte")
    o2gear0__lte = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="lte")
    o2gear0__gt = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="gt")
    o2gear0__lt = django_filters.NumberFilter(field_name="o2gear0", lookup_expr="lt")
    o2gear0__null = django_filters.BooleanFilter(
        field_name="o2gear0", lookup_expr="isnull"
    )
    o2gear0__not_null = django_filters.BooleanFilter(
        field_name="o2gear0", lookup_expr="isnull", exclude=True
    )

    o2gear1 = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="exact")
    o2gear1__gte = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="gte")
    o2gear1__lte = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="lte")
    o2gear1__gt = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="gt")
    o2gear1__lt = django_filters.NumberFilter(field_name="o2gear1", lookup_expr="lt")
    o2gear1__null = django_filters.BooleanFilter(
        field_name="o2gear1", lookup_expr="isnull"
    )
    o2gear1__not_null = django_filters.BooleanFilter(
        field_name="o2gear1", lookup_expr="isnull", exclude=True
    )

    o2bot0 = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="exact")
    o2bot0__gte = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="gte")
    o2bot0__lte = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="lte")
    o2bot0__gt = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="gt")
    o2bot0__lt = django_filters.NumberFilter(field_name="o2bot0", lookup_expr="lt")
    o2bot0__null = django_filters.BooleanFilter(
        field_name="o2bot0", lookup_expr="isnull"
    )
    o2bot0__not_null = django_filters.BooleanFilter(
        field_name="o2bot0", lookup_expr="isnull", exclude=True
    )

    o2bot1 = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="exact")
    o2bot1__gte = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="gte")
    o2bot1__lte = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="lte")
    o2bot1__gt = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="gt")
    o2bot1__lt = django_filters.NumberFilter(field_name="o2bot1", lookup_expr="lt")
    o2bot1__null = django_filters.BooleanFilter(
        field_name="o2bot1", lookup_expr="isnull"
    )
    o2bot1__not_null = django_filters.BooleanFilter(
        field_name="o2bot1", lookup_expr="isnull", exclude=True
    )

    o2surf0 = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="exact")
    o2surf0__gte = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="gte")
    o2surf0__lte = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="lte")
    o2surf0__gt = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="gt")
    o2surf0__lt = django_filters.NumberFilter(field_name="o2surf0", lookup_expr="lt")
    o2surf0__null = django_filters.BooleanFilter(
        field_name="o2surf0", lookup_expr="isnull"
    )
    o2surf0__not_null = django_filters.BooleanFilter(
        field_name="o2surf0", lookup_expr="isnull", exclude=True
    )

    o2surf1 = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="exact")
    o2surf1__gte = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="gte")
    o2surf1__lte = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="lte")
    o2surf1__gt = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="gt")
    o2surf1__lt = django_filters.NumberFilter(field_name="o2surf1", lookup_expr="lt")
    o2surf1__null = django_filters.BooleanFilter(
        field_name="o2surf1", lookup_expr="isnull"
    )
    o2surf1__not_null = django_filters.BooleanFilter(
        field_name="o2surf1", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = FN121Limno
        fields = [
            "o2gear0",
            "o2bot0",
            "o2bot1",
            "o2surf0",
            "o2surf1",
        ]
