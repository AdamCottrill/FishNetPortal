"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN121ElectroFishing
from rest_framework import generics

from ...filters import FN121ElectroFishingFilter
from ..serializers import FN121ElectroFishingReadOnlySerializer
from ..utils import LargeResultsSetPagination


class FN121ElectroFishingList(generics.ListAPIView):
    """A read-only endpoint for ElectroFishing data.  Accepts all of the query
    parmeters as FN121, with addition of 'gte', 'gt', 'lt', 'lte',
    'null' and 'not_null' arguments for each electrofishinglogilal parameter.
    """

    serializer_class = FN121ElectroFishingReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121ElectroFishingFilter

    queryset = (
        FN121ElectroFishing.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(prj_cd=F("sample__project__prj_cd"), sam=F("sample__sam"))
        .values(
            "prj_cd",
            "sam",
            "shock_sec",
            "waveform",
            "volts_min",
            "volts_max",
            "volts_mean",
            "amps_min",
            "amps_max",
            "amps_mean",
            "power_min",
            "power_max",
            "power_mean",
            "conduct",
            "turbidity",
            "pulse_dur",
            "pulse_pattern",
            "freq",
            "anodes",
            "num_netters",
            "comment",
            "slug",
        )
    )
