"""Views for common api endpoints - species, lakes, grids and management units."""

from django.contrib.auth import get_user_model
from rest_framework import generics

from common.models import Species

from ...filters import SpeciesFilter, UserFilter

from ..permissions import ReadOnly
from ..serializers import SpeciesSerializer, UserSerializer
from ..utils import StandardResultsSetPagination


User = get_user_model()


class SpeciesListView(generics.ListAPIView):
    """A read only end point to return lists of species - accepts case
    insensitve partial match filters for species code, scientific name,
    and common name."""

    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    filterset_class = SpeciesFilter


class ProjectLeadListView(generics.ListAPIView):
    """a simple, read only list view to return all of project leads from
    our database.  Accepts filters for status = active or all.
    Returns username, first name and lastname."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    # pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    filterset_class = UserFilter

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
