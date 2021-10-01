"""Views for common api endpoints - species, lakes, grids and management units."""

from fn_portal.api.serializers.common_serializers import LakeExtentSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics

from common.models import Species, Lake

from ...filters import SpeciesFilter, UserFilter

from ..permissions import ReadOnly
from ..serializers import SpeciesSerializer, UserSerializer, LakeExtentSerializer
from ..utils import StandardResultsSetPagination


User = get_user_model()


class SpeciesListView(generics.ListAPIView):
    """
    A read only end point to return lists of species - accepts case
    insensitve partial match filters for species code, scientific name,
    and common name.
    """

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    filterset_class = SpeciesFilter


class LakeExtentListView(generics.ListAPIView):
    """
    A read only end point to return lists our lakes - lake name,
    abbreviation, and the extents of the *Ontario* waters.  Used by the
    Project Setup wizard to ensure spatial strata are withing the
    bounds of the lake.

    This view does not currently accept any filters or parameters.
    All of the lakes are always returned.

    """

    pagination_class = None
    queryset = Lake.objects.all()
    serializer_class = LakeExtentSerializer
    permission_classes = [ReadOnly]


class ProjectLeadListView(generics.ListAPIView):
    """
    A simple, read only list view to return all of project leads from
    our database.  Accepts filters for status = active or all.
    Returns username, first name and lastname.
    """

    serializer_class = UserSerializer
    permission_classes = [ReadOnly]
    filterset_class = UserFilter
    pagination_class = None

    def get_queryset(self):
        """by default, we only want to return active users unless the request
        includes an argument for all users (e.g. - for historical
        projects).

        """
        all = self.request.query_params.get("all", False)

        if bool(all):
            queryset = User.objects.all()
        else:
            queryset = User.objects.filter(is_active=True)

        return queryset
