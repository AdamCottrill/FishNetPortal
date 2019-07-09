"""Views for api endpoints."""

from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    FN011Serializer,
    FN121Serializer,
    FN122Serializer,
    FN123Serializer,
    FN125Serializer,
)
from .filters import FN011Filter
from fn_portal.models import FN011, FN121, FN122, FN123, FN125, FN_Tags


# ViewSets define the view behavior.
class FN011ViewSet(viewsets.ModelViewSet):
    queryset = FN011.objects.all()
    serializer_class = FN011Serializer
    filterset_class = FN011Filter
    lookup_field = "slug"
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):

        queryset = FN011.objects.all()
        # finally django-filter
        filtered_list = FN011Filter(self.request.GET, queryset=queryset)

        return filtered_list.qs


class FN121ViewSet(viewsets.ModelViewSet):
    queryset = FN121.objects.all()
    serializer_class = FN121Serializer

    # lookup_field = "slug"


class NetSetList(generics.ListAPIView):
    """A view to return all of the net sets associated with a project"""

    serializer_class = FN121Serializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs["slug"]
        slug = slug.lower()
        return FN121.objects.filter(project__slug=slug)


class EffortList(generics.ListAPIView):
    """A view to return all of the catch counts associated with a project

    """

    serializer_class = FN122Serializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs["slug"]
        slug = slug.lower()
        sam = self.kwargs["sample"]

        queryset = FN122.objects.select_related("sample", "sample__project").filter(
            sample__project__slug=slug, sample__sam=sam
        )

        return queryset


class CatchCountList(generics.ListAPIView):
    """A view to return all of the catch counts associated with a project

    TODO: filter by SAM, EFF, SPC (and maybe GRP?)
"""

    serializer_class = FN123Serializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs["slug"]
        slug = slug.lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        queryset = (
            FN123.objects.select_related(
                "species", "effort", "effort__sample", "effort__sample__project"
            )
            .filter(effort__sample__project__slug=slug)
            .exclude(species__species_code=0)
        )

        if sam:
            queryset = queryset.filter(effort__sample__sam=sam)
        if eff:
            queryset = queryset.filter(effort__eff=eff)

        return queryset


class BioSampleList(generics.ListAPIView):
    """A view to return all of the catch counts associated with a project

     TODO: filter by SAM, EFF, SPC, (and maybe GRP?)

    """

    serializer_class = FN125Serializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        slug = self.kwargs["slug"]
        slug = slug.lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        # TODO - prefetch_related lamprey, tags (and maybe someday age estimates?)
        queryset = (
            FN125.objects.select_related(
                "catch",
                "catch__species",
                "catch__effort__sample",
                "catch__effort__sample__project",
            )
            .prefetch_related("tags")
            .filter(catch__effort__sample__project__slug=slug)
        )

        if sam:
            queryset = queryset.filter(catch__effort__sample__sam=sam)
        if eff:
            queryset = queryset.filter(catch__effort__eff=eff)
        if spc:
            queryset = queryset.filter(catch__species__species_code=spc)
        if grp:
            queryset = queryset.filter(catch__grp=grp)

        return queryset
