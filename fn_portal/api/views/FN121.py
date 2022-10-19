"""Views for api endpoints."""

from common.models import ManagementUnit
from django.db.models import Prefetch
from django.http import Http404
from fn_portal.models import FN011, FN121
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from ...filters import FN121Filter
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import FN121PostSerializer, FN121ReadOnlySerializer, FN121Serializer
from ..utils import LargeResultsSetPagination, StandardResultsSetPagination


class NetSetList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN121ReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121Filter

    def get_queryset(self):

        mu_type = self.request.query_params.get("mu_type")

        if mu_type:
            mus = ManagementUnit.objects.filter(mu_type=mu_type).defer("geom")
        else:
            mus = ManagementUnit.objects.filter(
                lake_management_unit_type__primary=True
            ).defer("geom")

        prefetched = Prefetch("management_units", queryset=mus, to_attr="mu")

        queryset = (
            (
                FN121.objects.select_related(
                    "project", "grid5", "grid5__lake", "ssn", "subspace", "mode"
                )
                .prefetch_related(prefetched)
                .defer(
                    "grid5__geom",
                    "grid5__envelope",
                    "grid5__centroid",
                    "grid5__lake__geom",
                    "grid5__lake__geom_ontario",
                    "grid5__lake__envelope",
                    "grid5__lake__envelope_ontario",
                    "grid5__lake__centroid",
                    "grid5__lake__centroid_ontario",
                )
            )
            .order_by("slug")
            .all()
            .distinct()
        )

        return queryset


# ========================================================
#      RETRIEVE-UPDATE-DESTROY

# these views will be used to get, update and delete individual
# records for netsets, efforts, catch counts and bio-samples.


class FN121ListView(generics.ListCreateAPIView):
    """An api end point for listing net sets within a project. A new net
    set can be created by posting to this endpoint.  A get request
    will return a json response containing all of the net sets
    associated with the project identifed by the project code in the url.

    TODO:

    + add filters for gear type, depth, active (lifttime=null)

    """

    permission_classes = [IsAdminUser | IsPrjLeadCrewOrAdminOrReadOnly]
    filterset_class = FN121Filter
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """our get and post serializiers have different fields for ssn, space
        and mode - get has object labels, post expects slugs."""
        if self.request.method == "GET":
            return FN121Serializer
        return FN121PostSerializer

    def get_project(self):
        """

        Arguments:
        - `self`:
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        try:
            project = FN011.objects.defer(
                "lake__geom",
                "lake__geom_ontario",
                "lake__envelope",
                "lake__envelope_ontario",
                "lake__centroid",
                "lake__centroid_ontario",
            ).get(slug=prj_cd)

            return project

        except FN011.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return a list of all the net sets for a project
        as determined by the slug portion of the URL.
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        queryset = (
            FN121.objects.filter(project__slug=prj_cd)
            .select_related("grid5", "grid5__lake")
            .defer(
                "grid5__geom",
                "grid5__envelope",
                "grid5__centroid",
                "grid5__lake__geom",
                "grid5__lake__geom_ontario",
                "grid5__lake__envelope",
                "grid5__lake__envelope_ontario",
                "grid5__lake__centroid",
                "grid5__lake__centroid_ontario",
            )
        )

        return queryset

    def get_serializer_context(self):
        """to create a new net set, we have to make the project available in
        the serializer's context"""

        context = super(FN121ListView, self).get_serializer_context()
        project = self.get_project()
        context.update({"project": project})
        return context


class FN121DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual net sets with GET, PATCH, and DELETE requests.
    Requires a unique slug value to identify the net set.  THe slug is
    of the form: <prj_cd>-<sam>.

    e.g. - lha_ia01_023-1

    """

    permission_classes = [IsAdminUser | IsPrjLeadCrewOrAdminOrReadOnly]
    # serializer_class = FN121PostSerializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN121.objects.all()

    def get_serializer_class(self):
        """our get and post serializiers have different fields for ssn, space
        and mode - get has object labels, post expects slugs."""
        if self.request.method == "GET":
            return FN121Serializer
        return FN121PostSerializer
