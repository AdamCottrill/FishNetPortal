import django_filters

from ..models import FN026
from .common_filters import NumberInFilter, ValueInFilter


class FN026SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    spatial attributes.

    # TODO - add filters by roi or other spatial attributes"""

    space = ValueInFilter(field_name="space")
    space__not = ValueInFilter(field_name="space", exclude=True)

    space__like = django_filters.CharFilter(field_name="space", lookup_expr="icontains")

    space__not_like = django_filters.CharFilter(
        field_name="space", lookup_expr="icontains", exclude=True
    )

    space_des = ValueInFilter(field_name="space_des")
    space_des__not = ValueInFilter(field_name="space_des", exclude=True)

    space_des__like = django_filters.CharFilter(
        field_name="space_des", lookup_expr="icontains"
    )

    space_des__not_like = django_filters.CharFilter(
        field_name="space_des", lookup_expr="icontains", exclude=True
    )

    class Meta:
        model = FN026
        fields = ["space", "space_des"]


class FN026Filter(FN026SubFilter):
    """Extends the FN026SubFilter to include additional fields that
    are associated with parent objects.
    """

    # FN011 ATTRIBUTES
    year = django_filters.CharFilter(field_name="project__year", lookup_expr="exact")
    year__gte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="gte"
    )
    year__lte = django_filters.NumberFilter(
        field_name="project__year", lookup_expr="lte"
    )

    year__gt = django_filters.NumberFilter(field_name="project__year", lookup_expr="gt")
    year__lt = django_filters.NumberFilter(field_name="project__year", lookup_expr="lt")

    prj_date0 = django_filters.DateFilter(
        field_name="project__prj_date0", help_text="format: yyyy-mm-dd"
    )
    prj_date0__gte = django_filters.DateFilter(
        field_name="project__prj_date0",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date0__lte = django_filters.DateFilter(
        field_name="project__prj_date0",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_date1 = django_filters.DateFilter(
        field_name="project__prj_date1", help_text="format: yyyy-mm-dd"
    )
    prj_date1__gte = django_filters.DateFilter(
        field_name="project__prj_date1",
        lookup_expr="gte",
        help_text="format: yyyy-mm-dd",
    )
    prj_date1__lte = django_filters.DateFilter(
        field_name="project__prj_date1",
        lookup_expr="lte",
        help_text="format: yyyy-mm-dd",
    )

    prj_cd = ValueInFilter(field_name="project__prj_cd")
    prj_cd__not = ValueInFilter(field_name="project__prj_cd", exclude=True)

    prj_cd__like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains"
    )

    prj_cd__not_like = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="icontains", exclude=True
    )

    prj_cd__endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith"
    )
    prj_cd__not_endswith = django_filters.CharFilter(
        field_name="project__prj_cd", lookup_expr="endswith", exclude=True
    )

    prj_nm__like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains"
    )

    prj_nm__not_like = django_filters.CharFilter(
        field_name="project__prj_nm", lookup_expr="icontains", exclude=True
    )

    prj_ldr = django_filters.CharFilter(
        field_name="project__prj_ldr__username", lookup_expr="iexact"
    )

    protocol = ValueInFilter(field_name="project__protocol__abbrev")
    protocol__not = ValueInFilter(field_name="project__protocol__abbrev", exclude=True)

    lake = ValueInFilter(field_name="project__lake__abbrev")

    lake__not = ValueInFilter(field_name="project__lake__abbrev", exclude=True)

    class Meta:
        model = FN026
        fields = [
            "project__year",
            "project__prj_cd",
            "project__lake",
            "project__source",
            "space",
            "space_des",
        ]
