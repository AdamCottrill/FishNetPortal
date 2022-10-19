"""Views for api endpoints for our FN0 models."""


from django.db.models import F


from fn_portal.models import (
    FN026,
    FN026Subspace,
)
from rest_framework import generics

from ...filters import FN026Filter, FN026SubspaceFilter
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import (
    FN026ListSerializer,
    FN026Serializer,
    FN026SubspaceSerializer,
)
from ..utils import StandardResultsSetPagination


class FN026ListView(generics.ListAPIView):
    """an api end point to list all of the spaces (FN026) associated with a
    project."""

    serializer_class = FN026ListSerializer
    filterset_class = FN026Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""

        qs = FN026.objects.all().select_related("project")
        prj_cd = self.kwargs.get("prj_cd")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs


class FN026DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for
    space/area objects associated with a specfic project

    """

    lookup_field = "space"
    serializer_class = FN026Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(project__slug=prj_cd.lower())


class FN026SubspaceListView(generics.ListAPIView):
    """an api end point to list all of the subspaces.  Optional
    arguments for prj_cd and space allow this endpoint to return all
    of the subspaces associated with a project, or all of the
    subspaces for a space within a project.

    """

    serializer_class = FN026SubspaceSerializer
    filterset_class = FN026SubspaceFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""

        qs = FN026Subspace.objects.annotate(
            prj_cd=F("space__project__prj_cd"), space_code=F("space__space")
        ).select_related("space", "space__project")
        prj_cd = self.kwargs.get("prj_cd")
        space = self.kwargs.get("space")
        if prj_cd:
            qs = qs.filter(space__project__prj_cd=prj_cd)
        if space:
            qs = qs.filter(space__space=space)

        return qs.values(
            "prj_cd",
            "space_code",
            "subspace",
            "subspace_des",
            "subspace_wt",
            "dd_lat",
            "dd_lon",
            "slug",
            "id",
        )
