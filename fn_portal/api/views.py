"""Views for api endpoints."""

from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import FN011Serializer, FN121Serializer
from .filters import FN011Filter
from fn_portal.models import FN011, FN121


# ViewSets define the view behavior.
class FN011ViewSet(viewsets.ModelViewSet):
    queryset = FN011.objects.all()
    serializer_class = FN011Serializer
    lookup_field = "prj_cd"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        queryset = FN011.objects.all()
        # finally django-filter
        filtered_list = FN011Filter(self.request.GET, queryset=queryset)

        return filtered_list.qs


class FN121ViewSet(viewsets.ModelViewSet):
    queryset = FN121.objects.all()
    serializer_class = FN121Serializer
    filterset_class = FN011Filter
    # lookup_field = "prj_cd"
