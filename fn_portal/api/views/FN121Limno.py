"""Views for api endpoints."""

from django.db.models import F
from fn_portal.models import FN121Limno
from rest_framework import generics

from ...filters import FN121LimnoFilter
from ..serializers import FN121LimnoSerializer
from ..utils import LargeResultsSetPagination


class FN121LimnoList(generics.ListAPIView):
    """A read-only endpoint for Limno data.  Accepts all of the query
    parmeters as FN121, with addition of 'gte', 'gt', 'lt', 'lte',
    'null' and 'not_null' arguments for each limnologilal parameter.
    """

    serializer_class = FN121LimnoSerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121LimnoFilter

    queryset = (
        FN121Limno.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(prj_cd=F("sample__project__prj_cd"), sam=F("sample__sam"))
        .values(
            "prj_cd",
            "sam",
            "o2gear0",
            "o2gear1",
            "o2bot0",
            "o2bot1",
            "o2surf0",
            "o2surf1",
            "slug",
        )
    )
