from django.db.models import F
from fn_portal.models import FN124
from rest_framework import generics

from ...filters import FN124Filter
from ..serializers import FN124Serializer
from ..utils import LargeResultsSetPagination


class LengthTallyList(generics.ListAPIView):
    """A read-only endpoint to return length tally objects.  Accepts query
    parameter filters for attributes of the length tally, the catch,
    the effort, the sample and the project.

    """

    serializer_class = FN124Serializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN124Filter

    queryset = (
        FN124.objects.select_related(
            "catch__species",
            "catch__effort",
            "catch__effort__sample",
            "catch__effort__sample__project",
        )
        .exclude(catch__species__spc="000")
        .annotate(
            prj_cd=F("catch__effort__sample__project__prj_cd"),
            sam=F("catch__effort__sample__sam"),
            eff=F("catch__effort__eff"),
            spc=F("catch__species__spc"),
            grp=F("catch__grp"),
        )
        .order_by("slug")
    )
