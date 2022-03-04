import django_filters

from ..models import FN012, FN012Base, FN012Protocol
from .common_filters import NumberInFilter, ValueInFilter


class FN012SubFilter(django_filters.FilterSet):
    """A fitlerset that allows us to select subsets of net set objects by
    net set attributes."""

    grp = ValueInFilter(field_name="grp")
    grp__not = ValueInFilter(field_name="grp", exclude=True)

    spc = ValueInFilter(field_name="species__spc")
    spc__not = ValueInFilter(field_name="species__spc", exclude=True)

    spc_nmco__like = django_filters.CharFilter(
        field_name="species__spc_nmco", lookup_expr="icontains"
    )

    spc_nmco__not_like = django_filters.CharFilter(
        field_name="species__spc_nmco", lookup_expr="icontains", exclude=True
    )

    spc_nmsc__like = django_filters.CharFilter(
        field_name="species__spc_nmsc", lookup_expr="icontains"
    )

    spc_nmsc__not_like = django_filters.CharFilter(
        field_name="species__spc_nmsc", lookup_expr="icontains", exclude=True
    )

    grp = ValueInFilter(field_name="grp")
    grp__not = ValueInFilter(field_name="grp", exclude=True)

    biosam = ValueInFilter(field_name="biosam")
    biosam__not = ValueInFilter(field_name="biosam", exclude=True)

    sizsam = ValueInFilter(field_name="sizsam")
    sizsam__not = ValueInFilter(field_name="sizsam", exclude=True)

    sizatt = ValueInFilter(field_name="sizatt")
    sizatt__not = ValueInFilter(field_name="sizatt", exclude=True)

    fdsam = ValueInFilter(field_name="fdsam")
    fdsam__not = ValueInFilter(field_name="fdsam", exclude=True)

    spcmrk = ValueInFilter(field_name="spcmrk")
    spcmrk__not = ValueInFilter(field_name="spcmrk", exclude=True)

    agedec = ValueInFilter(field_name="agedec")
    agedec__not = ValueInFilter(field_name="agedec", exclude=True)

    lamsam = ValueInFilter(field_name="lamsam")
    lamsam__not = ValueInFilter(field_name="lamsam", exclude=True)

    class Meta:
        model = FN012
        fields = [
            "species",
            "grp",
            "biosam",
            "sizsam",
            "sizatt",
            "fdsam",
            "spcmrk",
            "agedec",
            "lamsam",
        ]


class FN012Filter(FN012SubFilter):
    """Extends the FN012SubFilter to include additional fields that
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
        model = FN012
        fields = [
            "project__year",
            "project__prj_cd",
            "project__lake",
            "project__source",
        ]


class FN012ProtocolFilter(FN012SubFilter):
    """Extends the FN012SubFilter to include additional fields that
    are associated with parent objects.
    """

    protocol = ValueInFilter(field_name="protocol__abbrev")
    protocol__not = ValueInFilter(field_name="protocol__abbrev", exclude=True)

    lake = ValueInFilter(field_name="lake__abbrev")
    lake__not = ValueInFilter(field_name="lake__abbrev", exclude=True)

    class Meta:
        model = FN012Protocol
        fields = ["protocol", "lake"]
