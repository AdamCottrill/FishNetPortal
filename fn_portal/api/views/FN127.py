"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN127
from rest_framework import generics

from ...filters import FN127Filter
from ..serializers import FN127Serializer
from ..utils import XLargeResultsSetPagination


class FN127ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return age estimates objects.

    TODO - add filter for FN126 objects

    """

    serializer_class = FN127Serializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN127Filter
    queryset = (
        FN127.objects.select_related(
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
            "ageid",
            "agemt",
            "xagem",
            "agea",
            "preferred",
            "conf",
            "nca",
            "edge",
            "agestrm",
            "agelake",
            "spawnchkcnt",
            "age_fail",
            "comment7",
            "slug",
        )
    )
