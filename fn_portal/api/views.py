"""Views for api endpoints."""

from rest_framework import viewsets, generics

from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from .serializers import (
    SpeciesSerializer,
    FN011Serializer,
    FN121Serializer,
    FN122Serializer,
    FN123Serializer,
    FN125Serializer,
)
from ..filters import FN011Filter
from fn_portal.models import Species, FN011, FN121, FN122, FN123, FN125, FN125Tag


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class SpeciesList(generics.ListAPIView):
    queryset = Species.objects.all()
    serializer_class = SpeciesSerializer


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
    permission_classes = [IsAuthenticatedOrReadOnly]
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


class FN121ViewSet(viewsets.ModelViewSet):
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

    serializer_class = FN121Serializer
    pagination_class = StandardResultsSetPagination

    # lookup_field = "slug"


class NetSetList(generics.ListCreateAPIView):
    """A view to return all of the net sets associated with a project.

    TODO: add filters for gear type, depth, active (lifttime=null)"""

    serializer_class = FN121Serializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        """to create a new net set, we have to make the project available in
        the serializer's context"""

        context = super(NetSetList, self).get_serializer_context()
        slug = self.kwargs.get("slug", "").lower()

        project = FN011.objects.defer(
            "lake__geom",
            "lake__geom_ontario",
            "lake__envelope",
            "lake__envelope_ontario",
            "lake__centroid",
            "lake__centroid_ontario",
        ).get(slug=slug)

        context.update({"project": project})
        return context

    def get_queryset(self):
        """
        This view should return a list of all the net sets for a project
        as determined by the slug portion of the URL.
        """
        slug = self.kwargs.get("slug", "")
        slug = slug.lower()

        queryset = (
            FN121.objects.filter(project__slug=slug)
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
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
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
        sam = self.kwargs["sample"]
        eff = self.kwargs.get("effort")

        effort = FN122.objects.select_related("sample", "sample__project").get(
            sample__project__slug=slug, sample__sam=sam, eff=eff
        )

        context.update({"effort": effort})

        return context


class BioSampleList(generics.ListCreateAPIView):
    """A view to return all of the catch counts associated with a project

     TODO: filter by SAM, EFF, SPC, (and maybe GRP?)

    """

    serializer_class = FN125Serializer

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(BioSampleList, self).get_serializer_context()
        slug = self.kwargs.get("slug", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        context.update(
            {
                "catch_count": FN123.objects.get(
                    effort__sample__project__slug=slug,
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
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs.get("slug", "")
        slug = slug.lower()

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
            .filter(catch__effort__sample__project__slug=slug)
        )

        if sam:
            queryset = queryset.filter(catch__effort__sample__sam=sam)
        if eff:
            queryset = queryset.filter(catch__effort__eff=eff)
        if spc:
            queryset = queryset.filter(catch__species__spc=spc)
        if grp:
            queryset = queryset.filter(catch__grp=grp)

        return queryset


# ========================================================
#      RETRIEVE-UPDATE-DESTROY

# these views will be used to get, update and delete individual
# records for netsets, efforts, catch counts and bio-samples.


class FN121DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual net sets with GET, PATCH, and DELETE requests.
    Requires a unique slug value to identify the net set.  THe slug is
    of the form: <prj_cd>-<sam>.

    e.g. - lha_ia01_023-1

    """

    serializer_class = FN121Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN121.objects.all()


class FN122DetailView(generics.RetrieveUpdateDestroyAPIView):

    """An classed based view that provides a way to retrieve, update and
    delete individual efforts within a net set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the effort
    set.  THe slug is of the form: <prj_cd>-<sam>-<eff>.

    e.g. - lha_ia01_023-1-051

    """

    serializer_class = FN122Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN122.objects.all()


class FN123DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual catch counts within an effort set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the catch count
    (including both species and group code).  THe slug is of the form:
    <prj_cd>-<sam>-<eff>-<spc>-<grp>.

    e.g. - lha_ia01_023-1-051-331-00

    """

    serializer_class = FN123Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN123.objects.all()


class FN125DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual fish within an catch count with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the
    fish.  THe slug is of the form: <prj_cd>-<sam>-<eff>-<spc>-<grp>-<fish>.

    e.g. - lha_ia01_023-1-051-331-00-1

    """

    permission_classes = [AllowAny]
    serializer_class = FN125Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN125.objects.all()
