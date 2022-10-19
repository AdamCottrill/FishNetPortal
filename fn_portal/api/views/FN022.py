"""Views for api endpoints for our FN0 models."""

from fn_portal.models import FN022
from rest_framework import generics

from ...filters import FN022Filter

from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import FN022ListSerializer, FN022Serializer

from ..utils import StandardResultsSetPagination


class FN022ListView(generics.ListAPIView):
    """an api end point to list all of the seasons (FN022) associated with a
    project."""

    serializer_class = FN022ListSerializer
    filterset_class = FN022Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd")
        qs = FN022.objects.all().select_related("project")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs


class FN022DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for season
    objects associated with a specfic project"""

    lookup_field = "ssn"
    serializer_class = FN022Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this project."""

        prj_cd = self.kwargs.get("prj_cd")
        return FN022.objects.filter(project__slug=prj_cd.lower()).select_related(
            "project"
        )
