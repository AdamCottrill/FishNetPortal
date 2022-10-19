"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN126
from rest_framework import generics

from ...filters import FN126Filter
from ..serializers import FN126Serializer
from ..utils import XLargeResultsSetPagination


class FN126ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects."""

    serializer_class = FN126Serializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN126Filter
    queryset = (
        FN126.objects.select_related(
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
            "food",
            "taxon",
            "fdcnt",
            "comment6",
            "slug",
        )
    )
