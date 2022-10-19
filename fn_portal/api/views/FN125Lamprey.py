from django.db.models import F
from fn_portal.models import FN125_Lamprey
from rest_framework import generics

from ...filters import FN125LampreyFilter
from ..serializers import FN125LampreySerializer
from ..utils import XLargeResultsSetPagination


class FN125LampreyReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects.

    TODO - add filter for FN125Lamprey objects

    """

    serializer_class = FN125LampreySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN125LampreyFilter
    queryset = (
        FN125_Lamprey.objects.select_related(
            "fish",
            "fish__catch",
            "fish__catch__species",
            "fish__catch__effort__sample",
            "fish__catch__effort__sample__project",
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("fish__catch__effort__sample__project__prj_cd"),
            sam=F("fish__catch__effort__sample__sam"),
            eff=F("fish__catch__effort__eff"),
            spc=F("fish__catch__species__spc"),
            grp=F("fish__catch__grp"),
            fishn=F("fish__fish"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fishn",
            "lamid",
            "xlam",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
            "slug",
        )
    )
