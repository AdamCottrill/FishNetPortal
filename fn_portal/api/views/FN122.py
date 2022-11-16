from django.db.models import F
from fn_portal.models import FN122
from rest_framework import generics

from ...filters import FN122Filter
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import FN122ReadOnlySerializer, FN122Serializer
from ..utils import XLargeResultsSetPagination


class EffortList(generics.ListAPIView):
    """A read-only endpoint to return effort (gill net panels or trap net
    lifts) objects.  Accepts query parameter filters for year, project
    codes, site depth, lift and set dates and times, gear types, and
    grid(s).

    """

    serializer_class = FN122ReadOnlySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN122Filter
    queryset = (
        FN122.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(prj_cd=F("sample__project__prj_cd"), sam=F("sample__sam"))
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "effdst",
            "grdep0",
            "grdep1",
            "grtem0",
            "grtem1",
            "waterhaul",
            "comment2",
            "slug",
        )
    )


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
