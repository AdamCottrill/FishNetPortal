"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN121Trawl
from rest_framework import generics

from ...filters import FN121TrawlFilter
from ..serializers import FN121TrawlReadOnlySerializer
from ..utils import LargeResultsSetPagination


class FN121TrawlList(generics.ListAPIView):
    """A read-only endpoint for Trawl data.  Accepts all of the query
    parmeters as FN121, with addition of 'gte', 'gt', 'lt', 'lte',
    'null' and 'not_null' arguments for each limnologilal parameter.
    """

    serializer_class = FN121TrawlReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121TrawlFilter

    queryset = (
        FN121Trawl.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(
            prj_cd=F("sample__project__prj_cd"),
            sam=F("sample__sam"),
            vessel_abbrev=F("vessel__abbrev"),
        )
        .values(
            "prj_cd",
            "sam",
            "vessel_abbrev",
            "vessel_speed",
            "vessel_direction",
            "warp",
            "slug",
        )
    )
