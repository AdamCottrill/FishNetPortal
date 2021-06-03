"""Views for api endpoints."""

from collections import OrderedDict

from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from common.models import Species
from fn_portal.models import (
    FN011,
    FN022,
    FN026,
    FN028,
    FN121,
    FN122,
    FN123,
    FN125,
    FN125Tag,
    FN125_Lamprey,
    FN126,
    FN127,
)

from ..filters import (
    FN011Filter,
    FN121Filter,
    FN122Filter,
    FN123Filter,
    FN125Filter,
    FN125LampreyFilter,
    FN125TagFilter,
    FN126Filter,
    FN127Filter,
    SpeciesFilter,
)
from .permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from .serializers import (
    FN011Serializer,
    FN022Serializer,
    FN026Serializer,
    FN028Serializer,
    FN121Serializer,
    FN122Serializer,
    FN123Serializer,
    FN125Serializer,
    FN125TagSerializer,
    FN125LampreySerializer,
    FN126Serializer,
    FN127Serializer,
    SpeciesSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class SpeciesList(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    filterset_class = SpeciesFilter


# ========================================================
#      READONLY ENDPOINTS


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


class NetSetList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN121Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN121Filter

    queryset = (
        (
            FN121.objects.select_related("grid", "grid__lake").defer(
                "grid__geom",
                "grid__envelope",
                "grid__centroid",
                "grid__lake__geom",
                "grid__lake__geom_ontario",
                "grid__lake__envelope",
                "grid__lake__envelope_ontario",
                "grid__lake__centroid",
                "grid__lake__centroid_ontario",
            )
        )
        .all()
        .distinct()
    )


class EffortList(generics.ListAPIView):
    """A read-only endpoint to return effort (gill net panels or trap net
    lifts) objects.  Accepts query parameter filters for year, project
    codes, site depth, lift and set dates and times, gear types, and
    grid(s).

    """

    serializer_class = FN122Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN122Filter
    queryset = FN122.objects.select_related("sample", "sample__project").distinct()


class CatchCountList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN123Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN123Filter

    queryset = (
        FN123.objects.select_related(
            "species", "effort", "effort__sample", "effort__sample__project"
        )
        .exclude(species__spc="000")
        .distinct()
    )


class BioSampleList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN125Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN125Filter
    queryset = FN125.objects.select_related(
        "catch",
        "catch__species",
        "catch__effort__sample",
        "catch__effort__sample__project",
    ).prefetch_related("fishtags", "lamprey_marks", "diet_data", "age_estimates")


class FN125LampreyReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects.

    TODO - add filter for FN125Lamprey objects

    """

    serializer_class = FN125LampreySerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN125LampreyFilter
    queryset = FN125_Lamprey.objects.select_related(
        "fish",
        "fish__catch",
        "fish__catch__species",
        "fish__catch__effort__sample",
        "fish__catch__effort__sample__project",
    )


class FN125TagReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return fish tags that have been either applied or recoved."""

    serializer_class = FN125TagSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN125TagFilter
    queryset = FN125Tag.objects.select_related(
        "fish",
        "fish__catch",
        "fish__catch__species",
        "fish__catch__effort__sample",
        "fish__catch__effort__sample__project",
    )


class FN126ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects."""

    serializer_class = FN126Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN126Filter
    queryset = FN126.objects.select_related(
        "fish",
        "fish__catch",
        "fish__catch__species",
        "fish__catch__effort__sample",
        "fish__catch__effort__sample__project",
    )


class FN127ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return age estimates objects.

    TODO - add filter for FN126 objects

    """

    serializer_class = FN127Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN127Filter
    queryset = FN127.objects.select_related(
        "fish",
        "fish__catch",
        "fish__catch__species",
        "fish__catch__effort__sample",
        "fish__catch__effort__sample__project",
    )


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

    serializer_class = FN121Serializer
    permission_classes = [IsAdminUser | IsPrjLeadCrewOrAdminOrReadOnly]
    filterset_class = FN121Filter
    pagination_class = StandardResultsSetPagination

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
            .select_related("grid", "grid__lake")
            .defer(
                "grid__geom",
                "grid__envelope",
                "grid__centroid",
                "grid__lake__geom",
                "grid__lake__geom_ontario",
                "grid__lake__envelope",
                "grid__lake__envelope_ontario",
                "grid__lake__centroid",
                "grid__lake__centroid_ontario",
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
    serializer_class = FN121Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN121.objects.all()


class FN122ListView(generics.ListCreateAPIView):
    """A view to return all of the efforts associated with a net set
    (within a project).

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN122Serializer

    def get_queryset(self):
        """
        This view should return a list of all the efforts for the net set identified by the
        project code and sample number.
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs["sample"]

        queryset = FN122.objects.select_related("sample", "sample__project").filter(
            sample__project__slug=prj_cd, sample__sam=sam
        )

        return queryset


class FN122DetailView(generics.RetrieveUpdateDestroyAPIView):

    """An classed based view that provides a way to retrieve, update and
    delete individual efforts within a net set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the effort
    set.  THe slug is of the form: <prj_cd>-<sam>-<eff>.

    e.g. - lha_ia01_023-1-051

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN122Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN122.objects.all()


class FN123ListView(generics.ListCreateAPIView):
    """A view to return all of the catch counts associated with a project

    TODO: filter by SAM, EFF, SPC (and maybe GRP?)
    """

    serializer_class = FN123Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        queryset = (
            FN123.objects.select_related(
                "species", "effort", "effort__sample", "effort__sample__project"
            )
            .filter(
                effort__sample__project__slug=prj_cd,
                effort__sample__sam=sam,
                effort__eff=eff,
            )
            .exclude(species__spc="000")
        )

        return queryset

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(FN123ListView, self).get_serializer_context()
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        if sam and eff:
            effort = FN122.objects.select_related("sample", "sample__project").get(
                sample__project__slug=prj_cd, sample__sam=sam, eff=eff
            )
            context.update({"effort": effort})

        return context


class FN123DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual catch counts within an effort set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the catch count
    (including both species and group code).  THe slug is of the form:
    <prj_cd>-<sam>-<eff>-<spc>-<grp>.

    e.g. - lha_ia01_023-1-051-331-00

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN123Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN123.objects.all()


class FN125ListView(generics.ListCreateAPIView):
    """A view to return all of the biosamples assocaited with an FN123
    record (by effort, species and grp) or to create a new FN125 record.

    if you are looking for all biosamples, see biosamples/ and
    <prj_cd>/biosamples endpoints.

    NOTES:

    + we could add filters to these at some point (find fish with
    specific attributes).

    + create has not yet been implemented.

    """

    serializer_class = FN125Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(FN125ListView, self).get_serializer_context()

        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        context.update(
            {
                "catch_count": FN123.objects.get(
                    effort__sample__project__slug=prj_cd,
                    effort__sample__sam=sam,
                    effort__eff=eff,
                    species__spc=spc,
                    grp=grp,
                )
            }
        )

        return context

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        queryset = (
            FN125.objects.select_related(
                "catch",
                "catch__species",
                "catch__effort__sample",
                "catch__effort__sample__project",
            )
            .prefetch_related("fishtags", "lamprey_marks", "diet_data", "age_estimates")
            .filter(
                catch__effort__sample__project__slug=prj_cd,
                catch__effort__sample__sam=sam,
                catch__effort__eff=eff,
                catch__species__spc=spc,
                catch__grp=grp,
            )
        )

        return queryset


class FN125DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual fish within an catch count with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the
    fish.  THe slug is of the form: <prj_cd>-<sam>-<eff>-<spc>-<grp>-<fish>.

    e.g. - lha_ia01_023-1-051-331-00-1

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN125Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN125.objects.all()
