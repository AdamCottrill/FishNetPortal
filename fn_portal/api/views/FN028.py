"""Views for api endpoints for our FN0 models."""

from fn_portal.models import FN028

from rest_framework import generics

from ...filters import (
    FN028Filter,
)
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import FN028ListSerializer, FN028Serializer

from ..utils import StandardResultsSetPagination


class FN028ListView(generics.ListAPIView):
    """an api end point to list all of the fishing modes (FN022) associated with a
    project."""

    serializer_class = FN028ListSerializer
    filterset_class = FN028Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""

        return FN028.objects.all().select_related("project", "gear")


class FN028DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for fishing mode
    objects associated with a specfic project.

    """

    lookup_field = "mode"
    serializer_class = FN028Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""

        qs = FN028.objects.all().select_related("project", "gear")
        prj_cd = self.kwargs.get("prj_cd")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs
