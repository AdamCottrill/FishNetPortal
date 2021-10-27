import django_filters

from ..models import Gear, GearEffortProcessType

from .common_filters import ValueInFilter


class GearFilter(django_filters.FilterSet):
    """A filter class for gear objects. Case insentitive filter for gear
    like and gear type, but gear codes - either a single gear code, or
    a comma separated list of gears must maatch exactly.  The
    get_queryset() method of the gearList view has methods to return
    all gears, or only those gears that are confirmed and active.

    """

    gr = ValueInFilter(field_name="gr_code")
    gr__like = django_filters.CharFilter(field_name="gr_code", lookup_expr="icontains")
    grtp = django_filters.CharFilter(field_name="grtp", lookup_expr="iexact")

    class Meta:
        model = Gear
        fields = ["gr_code", "grtp"]


class GearEffortProcessTypeFilter(django_filters.FilterSet):
    """A filter class for gear effort process type objects. This filter
    allows us to fetch the current 'approved' process types and
    associted efforts for each known gear type.

    """

    gr = ValueInFilter(field_name="gear__gr_code")
    gr__like = django_filters.CharFilter(
        field_name="gear__gr_code", lookup_expr="icontains"
    )
    grtp = django_filters.CharFilter(field_name="gear__grtp", lookup_expr="iexact")
    process_type = django_filters.CharFilter(
        field_name="process_type", lookup_expr="exact"
    )

    class Meta:
        model = GearEffortProcessType
        fields = ["gear__gr_code", "gear__grtp", "process_type"]
