from django.db.models import F
from fn_portal.models import FN123NonFish
from rest_framework import generics

from ...filters import FN123NonFishFilter
from ..serializers import FN123NonFishReadOnlySerializer
from ..utils import LargeResultsSetPagination


class FN123NonFishList(generics.ListAPIView):
    """A read-only endpoint to return non-fish objects (amphibians,
    birds and mammals).  Accepts query parameter filters for year,
    project codes, site depth, lift and set dates and times, gear
    types, and grid(s).

    """

    serializer_class = FN123NonFishReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN123NonFishFilter

    queryset = (
        FN123NonFish.objects.select_related(
            "taxon", "effort", "effort__sample", "effort__sample__project"
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("effort__sample__project__prj_cd"),
            sam=F("effort__sample__sam"),
            eff=F("effort__eff"),
            taxon_code=F("taxon__taxon"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "taxon_code",
            "catcnt",
            "mortcnt",
            "comment3",
            "slug",
        )
    )
