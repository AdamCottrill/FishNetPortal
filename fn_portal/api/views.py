"""Views for api endpoints."""

from collections import OrderedDict

from rest_framework import viewsets, generics

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response


from fn_portal.models import Species, FN011, FN121, FN122, FN123, FN125, FN125Tag
from .serializers import (
    SpeciesSerializer,
    FN011Serializer,
    FN121Serializer,
    FN122Serializer,
    FN123Serializer,
    FN125Serializer,
)
from ..filters import FN011Filter, FN121Filter, FN121InProjectFilter, FN125Filter
from .permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class SpeciesList(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer
    permission_classes = [ReadOnly]


# ViewSets define the view behavior.
class FN011ViewSet(viewsets.ModelViewSet):
    """An api endpoint for projects. """

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
    serializer_class = FN011Serializer
    filterset_class = FN011Filter
    lookup_field = "slug"
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

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
        # finally django-filter
        filtered_list = FN011Filter(self.request.GET, queryset=queryset)

        return filtered_list.qs


# class FN121ViewSet(viewsets.ModelViewSet):
#     queryset = (
#         FN121.objects.select_related("grid", "grid__lake").defer(
#             "grid__geom",
#             "grid__envelope",
#             "grid__centroid",
#             "grid__lake__geom",
#             "grid__lake__geom_ontario",
#             "grid__lake__envelope",
#             "grid__lake__envelope_ontario",
#             "grid__lake__centroid",
#             "grid__lake__centroid_ontario",
#         )
#     ).all()

#     serializer_class = FN121Serializer
#     pagination_class = StandardResultsSetPagination

#     # lookup_field = "slug"


# class NetSetList(generics.ListCreateAPIView):
#     """A view to return all of the net sets associated with a project.

#     TODO: add filters for gear type, depth, active (lifttime=null)"""

#     serializer_class = FN121Serializer
#     pagination_class = StandardResultsSetPagination

#     def get_serializer_context(self):
#         """to create a new net set, we have to make the project available in
#         the serializer's context"""

#         context = super(NetSetList, self).get_serializer_context()
#         slug = self.kwargs.get("slug", "").lower()

#         project = FN011.objects.defer(
#             "lake__geom",
#             "lake__geom_ontario",
#             "lake__envelope",
#             "lake__envelope_ontario",
#             "lake__centroid",
#             "lake__centroid_ontario",
#         ).get(slug=slug)

#         context.update({"project": project})
#         return context

#     def get_queryset(self):
#         """
#         This view should return a list of all the net sets for a project
#         as determined by the slug portion of the URL.
#         """
#         slug = self.kwargs.get("slug", "")
#         slug = slug.lower()

#         queryset = (
#             FN121.objects.filter(project__slug=slug)
#             .select_related("grid", "grid__lake")
#             .defer(
#                 "grid__geom",
#                 "grid__envelope",
#                 "grid__centroid",
#                 "grid__lake__geom",
#                 "grid__lake__geom_ontario",
#                 "grid__lake__envelope",
#                 "grid__lake__envelope_ontario",
#                 "grid__lake__centroid",
#                 "grid__lake__centroid_ontario",
#             )
#         )

#         return queryset


class EffortList(generics.ListCreateAPIView):
    """A view to return all of the efforts associated with a net set
    (within a project).

    """

    serializer_class = FN122Serializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs.get("slug", "")
        slug = slug.lower()
        sam = self.kwargs["sample"]

        queryset = FN122.objects.select_related("sample", "sample__project").filter(
            sample__project__slug=slug, sample__sam=sam
        )

        return queryset

    def get_serializer_context(self):
        """to create a new net set, we have to make the project available in
        the serializer's context"""

        context = super(EffortList, self).get_serializer_context()
        slug = self.kwargs.get("slug", "").lower()
        sam = self.kwargs["sample"]

        sample = FN121.objects.select_related("project").get(
            project__slug=slug, sam=sam
        )

        context.update({"sample": sample})
        return context


class CatchCountList(generics.ListCreateAPIView):
    """A view to return all of the catch counts associated with a project

    TODO: filter by SAM, EFF, SPC (and maybe GRP?)
"""

    serializer_class = FN123Serializer

    def get_queryset(self):
        """
        """
        slug = self.kwargs.get("slug", "")
        slug = slug.lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        queryset = (
            FN123.objects.select_related(
                "species", "effort", "effort__sample", "effort__sample__project"
            )
            .filter(effort__sample__project__slug=slug)
            .exclude(species__spc="000")
        )
        # this is also a hack - move the list by project out to its own endpoint!
        if sam:
            queryset = queryset.filter(effort__sample__sam=sam)
        if eff:
            queryset = queryset.filter(effort__eff=eff)

        return queryset

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(CatchCountList, self).get_serializer_context()
        slug = self.kwargs.get("slug", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        if sam and eff:
            effort = FN122.objects.select_related("sample", "sample__project").get(
                sample__project__slug=slug, sample__sam=sam, eff=eff
            )
            context.update({"effort": effort})

        return context


# class BioSampleList(generics.ListCreateAPIView):
#     """A view to return all of the catch counts associated with a project

#      TODO: filter by SAM, EFF, SPC, (and maybe GRP?)

#     """

#     serializer_class = FN125Serializer

#     def get_serializer_context(self):
#         """to create a new catch count, we have to make the effort available in
#         the serializer's context"""

#         context = super(BioSampleList, self).get_serializer_context()

#         slug = self.kwargs.get("slug", "").lower()
#         sam = self.kwargs.get("sample")
#         eff = self.kwargs.get("effort")
#         spc = self.kwargs.get("species")
#         grp = self.kwargs.get("group")

#         # This is a hack for today.  Move list by project out to their own endpoint.
#         if spc:
#             context.update(
#                 {
#                     "catch_count": FN123.objects.get(
#                         effort__sample__project__slug=slug,
#                         effort__sample__sam=sam,
#                         effort__eff=eff,
#                         species__spc=spc,
#                         grp=grp,
#                     )
#                 }
#             )

#         return context

#     def get_queryset(self):
#         """

#         """
#         slug = self.kwargs.get("slug", "")
#         slug = slug.lower()

#         sam = self.kwargs.get("sample")
#         eff = self.kwargs.get("effort")
#         spc = self.kwargs.get("species")
#         grp = self.kwargs.get("group")

#         queryset = (
#             FN125.objects.select_related(
#                 "catch",
#                 "catch__species",
#                 "catch__effort__sample",
#                 "catch__effort__sample__project",
#             )
#             .prefetch_related("fishtags", "lamprey_marks", "diet_data", "age_estimates")
#             .filter(catch__effort__sample__project__slug=slug)
#         )

#         if sam:
#             queryset = queryset.filter(catch__effort__sample__sam=sam)
#         if eff:
#             queryset = queryset.filter(catch__effort__eff=eff)
#         if spc:
#             queryset = queryset.filter(catch__species__spc=spc)
#         if grp:
#             queryset = queryset.filter(catch__grp=grp)

#         return queryset


# ========================================================
#      READONLY ENDPOINTS


class NetSetList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, proejct codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN121Serializer
    pagination_class = StandardResultsSetPagination
    filterset_class = FN121Filter

    queryset = (
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
    ).all()


class BioSampleList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, proejct codes, site depth, lift and
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
    filterset_class = FN121InProjectFilter
    pagination_class = StandardResultsSetPagination

    def get_project(self):
        """

        Arguments:
        - `self`:
        """

        prj_cd = self.kwargs.get("prj_cd", "").lower()

        project = FN011.objects.defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        ).get(slug=prj_cd)

        return project

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
        """
        """
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
        """

        """
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
