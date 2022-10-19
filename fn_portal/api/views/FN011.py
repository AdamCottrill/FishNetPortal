"""Views for api endpoints for our FN011 model objects."""

from fn_portal.models import FN011
from rest_framework import generics

from ...filters import FN011Filter
from ..permissions import ReadOnly
from ..serializers import FN011Serializer
from ..utils import StandardResultsSetPagination


class FN011ListView(generics.ListAPIView):
    """A read-only endpoint to return project objects.  Accepts query
    parameter filters for year, project codes, protocol, lake, gear types, and grid(s).
    """

    serializer_class = FN011Serializer
    filterset_class = FN011Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    queryset = (
        FN011.objects.select_related("protocol", "lake", "prj_ldr")
        .defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        )
        .all()
        .order_by("slug")
    )


class FN011DetailView(generics.RetrieveAPIView):
    """A read-only endpoint to return a single project object."""

    serializer_class = FN011Serializer
    lookup_field = "slug"
    permission_classes = [ReadOnly]

    queryset = (
        FN011.objects.select_related("protocol", "lake", "prj_ldr")
        .defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        )
        .all()
    )
