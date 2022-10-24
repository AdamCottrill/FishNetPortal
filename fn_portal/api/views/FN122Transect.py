from django.db.models import F
from fn_portal.models import FN122Transect
from rest_framework import generics

from ...filters import FN122TransectFilter
from ..serializers import FN122TransectReadOnlySerializer
from ..utils import XLargeResultsSetPagination


class FN122TransectList(generics.ListAPIView):
    """A read-only endpoint to return Fn122Transect objects.  Accepts
    query parameter filters for year, project codes, site depth, lift
    and set dates and times, gear types, and grid(s).

    """

    serializer_class = FN122TransectReadOnlySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN122TransectFilter
    queryset = (
        FN122Transect.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(prj_cd=F("sample__project__prj_cd"), sam=F("sample__sam"))
        .values(
            "id",
            "prj_cd",
            "sam",
            "track_id",
            "sidep",
            "timestamp",
            "geom",
            "comment",
            "slug",
        )
    )
