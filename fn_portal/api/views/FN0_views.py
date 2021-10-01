"""Views for api endpoints for our FN0 models."""


from rest_framework import generics

from fn_portal.models import FNProtocol, FN011, FN013, FN014, FN022, FN026, FN028

from ...filters import FN011Filter

from ..utils import StandardResultsSetPagination

from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import (
    FNProtocolSerializer,
    FN011Serializer,
    FN013Serializer,
    FN014Serializer,
    FN022Serializer,
    FN026Serializer,
    FN028Serializer,
)


class FNProtocolListView(generics.ListAPIView):
    """A read-only endpoint to return currently available protocols."""

    serializer_class = FNProtocolSerializer
    permission_classes = [ReadOnly]
    pagination_class = None

    def get_queryset(self):
        """by default, we only want to return active protocols
        that has been documented. If 'all' is specified, we return
        everything.

        Boolean confirmed arguments for active and confirmed allow us
        to refine which subsets are returned.

        """

        all = self.request.query_params.get("all", False)
        confirmed = self.request.query_params.get("confirmed")
        active = self.request.query_params.get("active")

        queryset = FNProtocol.objects.order_by("abbrev").all()

        if bool(all):
            return queryset
        else:
            if confirmed is None:
                queryset = queryset.filter(confirmed=True)
            else:
                confirmed = confirmed.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(confirmed=confirmed)

            if active is None:
                queryset = queryset.filter(active=True)
            else:
                active = active.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(active=active)

        return queryset


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
        .distinct()
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


class FN013ListView(generics.ListAPIView):
    """an api end point to list all of the gears  (FN013) associated with a
    project."""

    serializer_class = FN013Serializer

    def get_queryset(self):
        """"""

        prj_cd = self.kwargs.get("prj_cd")
        return FN013.objects.filter(project__slug=prj_cd.lower()).select_related(
            "project"
        )


class FN013DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for gear
    objects associated with a specfic project"""

    lookup_field = "gr"
    serializer_class = FN013Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this project."""

        prj_cd = self.kwargs.get("prj_cd")
        gr = self.kwargs.get("gr")
        return FN013.objects.filter(gr=gr, project__slug=prj_cd.lower()).select_related(
            "project"
        )


class FN014ListView(generics.ListAPIView):
    """an api end point to list all of the gear detail objects (FN014) associated with a
    project."""

    serializer_class = FN014Serializer

    def get_queryset(self):
        """"""

        prj_cd = self.kwargs.get("prj_cd")
        gr = self.kwargs.get("gr")
        return FN014.objects.filter(gear__project__slug=prj_cd.lower(), gear__gr=gr)


class FN014DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for gear panel
    objects associated with a specfic gear within a project"""

    lookup_field = "eff"
    serializer_class = FN014Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """return only those season objects associate with this project."""

        prj_cd = self.kwargs.get("prj_cd")
        gr = self.kwargs.get("gr")
        eff = self.kwargs.get("eff")
        return FN014.objects.filter(
            gear__project__slug=prj_cd.lower(), gear__gr=gr, eff=eff
        )


class FN022ListView(generics.ListAPIView):
    """an api end point to list all of the seasons (FN022) associated with a
    project."""

    serializer_class = FN022Serializer

    def get_queryset(self):
        """"""

        prj_cd = self.kwargs.get("prj_cd")
        return FN022.objects.filter(project__slug=prj_cd.lower()).select_related(
            "project"
        )


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


class FN026ListView(generics.ListAPIView):
    """an api end point to list all of the spaces (FN026) associated with a
    project."""

    serializer_class = FN026Serializer

    def get_queryset(self):
        """"""

        prj_cd = self.kwargs.get("prj_cd")
        return FN026.objects.filter(project__slug=prj_cd.lower())


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


class FN028ListView(generics.ListAPIView):
    """an api end point to list all of the fishing modes (FN022) associated with a
    project."""

    serializer_class = FN028Serializer

    def get_queryset(self):
        """"""

        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(project__slug=prj_cd.lower())


class FN028DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for fishing mode
    objects associated with a specfic project.

    """

    lookup_field = "mode"
    serializer_class = FN028Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd")
        return FN028.objects.filter(project__slug=prj_cd.lower())
