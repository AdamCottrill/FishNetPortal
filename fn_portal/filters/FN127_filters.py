import django_filters

from .common_filters import ValueInFilter, NumberInFilter

from ..models import FN127
from .FishAttr_filters import FishAttrFilters


class FN127Filter(FishAttrFilters):
    """A fitlerset that allows us to select subsets of FN127 table (age estimates/interpretations) by
    by attributes of the age estimates (FN127 data only)"""

    # preferred = True/False
    # agemt - in, like
    # xagem in and like
    # conf =, gte, lte, gt, lt
    # nca =, gte, lte, gt, lt
    # agea =, gte, lte, gt, lt
    # edge in

    # fish = slug__in

    preferred = django_filters.BooleanFilter(field_name="preferred")

    agemt = ValueInFilter(field_name="agemt")
    agemt__not = ValueInFilter(field_name="agemt", exclude=True)

    agemt__like = ValueInFilter(field_name="agemt", lookup_expr="icontains")

    xagem = ValueInFilter(field_name="xagem")
    xagem__not = ValueInFilter(field_name="xagem", exclude=True)
    xagem__like = ValueInFilter(field_name="xagem", lookup_expr="icontains")

    edge = ValueInFilter(field_name="edge")
    edge__not = ValueInFilter(field_name="edge", exclude=True)

    agea = django_filters.NumberFilter(field_name="agea")
    agea__gte = django_filters.NumberFilter(field_name="agea", lookup_expr="gte")
    agea__lte = django_filters.NumberFilter(field_name="agea", lookup_expr="lte")
    agea__gt = django_filters.NumberFilter(field_name="agea", lookup_expr="gt")
    agea__lt = django_filters.NumberFilter(field_name="agea", lookup_expr="lt")

    nca = django_filters.NumberFilter(field_name="nca")
    nca__gte = django_filters.NumberFilter(field_name="nca", lookup_expr="gte")
    nca__lte = django_filters.NumberFilter(field_name="nca", lookup_expr="lte")
    nca__gt = django_filters.NumberFilter(field_name="nca", lookup_expr="gt")
    nca__lt = django_filters.NumberFilter(field_name="nca", lookup_expr="lt")

    conf = django_filters.NumberFilter(field_name="conf")
    conf__gte = django_filters.NumberFilter(field_name="conf", lookup_expr="gte")
    conf__lte = django_filters.NumberFilter(field_name="conf", lookup_expr="lte")
    conf__gt = django_filters.NumberFilter(field_name="conf", lookup_expr="gt")
    conf__lt = django_filters.NumberFilter(field_name="conf", lookup_expr="lt")

    class Meta:
        model = FN127
        fields = ["conf", "nca", "agea", "edge", "xagem", "agemt", "preferred"]
