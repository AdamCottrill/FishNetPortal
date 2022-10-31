from django.db.models import F
from fn_portal.models import FN123
from rest_framework import generics

from ...filters import FN123Filter
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import FN123Serializer
from ..utils import LargeResultsSetPagination


class CatchCountList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN123Serializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN123Filter

    queryset = (
        FN123.objects.select_related(
            "species", "effort", "effort__sample", "effort__sample__project"
        )
        .exclude(species__spc="000")
        .order_by("slug")
        .annotate(
            prj_cd=F("effort__sample__project__prj_cd"),
            sam=F("effort__sample__sam"),
            eff=F("effort__eff"),
            spc=F("species__spc"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "catcnt",
            "catwt",
            "biocnt",
            "subwt",
            "subcnt",
            "comment3",
            "slug",
        )
    )


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
