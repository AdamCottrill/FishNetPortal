"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN121Trapnet
from rest_framework import generics

from ...filters import FN121TrapnetFilter
from ..serializers import FN121TrapnetReadOnlySerializer
from ..utils import LargeResultsSetPagination


class FN121TrapnetList(generics.ListAPIView):
    """A read-only endpoint for Trapnet data.  Accepts all of the query
    parmeters as FN121, with addition of 'gte', 'gt', 'lt', 'lte',
    'null' and 'not_null' arguments for each limnologilal parameter.
    """

    serializer_class = FN121TrapnetReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121TrapnetFilter

    queryset = (
        FN121Trapnet.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(
            prj_cd=F("sample__project__prj_cd"),
            sam=F("sample__sam"),
            bottom_type=F("bottom__abbrev"),
            cover_type=F("cover__abbrev"),
        )
        .values(
            "prj_cd",
            "sam",
            "bottom_type",
            "cover_type",
            "vegetation",
            "lead_angle",
            "leaduse",
            "distoff",
            "slug",
        )
    )
