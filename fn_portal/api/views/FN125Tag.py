"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN125Tag
from rest_framework import generics

from ...filters import FN125TagFilter
from ..serializers import FN125TagSerializer
from ..utils import XLargeResultsSetPagination


class FN125TagReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return fish tags that have been either
    applied or recoved."""

    serializer_class = FN125TagSerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN125TagFilter
    queryset = (
        FN125Tag.objects.select_related(
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
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "cwtseq",
            "tag_checked",
            "comment_tag",
            "slug",
        )
    )
