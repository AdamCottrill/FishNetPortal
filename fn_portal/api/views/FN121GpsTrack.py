from django.db.models import F
from fn_portal.models import FN121GpsTrack
from rest_framework import generics

from ...filters import FN121GpsTrackFilter
from ..serializers import FN121GpsTrackReadOnlySerializer
from ..utils import XLargeResultsSetPagination


class FN121GpsTrackList(generics.ListAPIView):
    """A read-only endpoint to return Fn121GpsTrack objects.  Accepts
    query parameter filters for year, project codes, site depth, lift
    and set dates and times, gear types, and grid(s).

    """

    serializer_class = FN121GpsTrackReadOnlySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN121GpsTrackFilter
    queryset = (
        FN121GpsTrack.objects.select_related("sample", "sample__project")
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
