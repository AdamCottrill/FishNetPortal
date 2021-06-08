"""Views for common api endpoints - species, lakes, grids and management units."""

from rest_framework import generics

from common.models import Species

from ...filters import SpeciesFilter

from ..permissions import ReadOnly
from ..serializers import SpeciesSerializer
from ..utils import StandardResultsSetPagination


class SpeciesListView(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    filterset_class = SpeciesFilter
