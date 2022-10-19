"""Views for api endpoints for our FN013 models."""

from django.db.models import F
from fn_portal.models import FN013, FN028
from rest_framework import generics

from ...filters import FN028Filter
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import FN013ListSerializer, FN013Serializer
from ..utils import StandardResultsSetPagination


class FN013ListView(generics.ListAPIView):
    """an api end point to list all of the gears (FN013) associated with a
    project. - this is actually a list of FN028 objects annotated with
    the associated project code and gear attributes to emulate the
    FN013 data.  the filters wouldn't work when the Gear objects where
    used.

    """

    serializer_class = FN013ListSerializer
    filterset_class = FN028Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    queryset = (
        FN028.objects.all()
        .select_related(
            "project",
            "gear",
        )
        .annotate(
            prj_cd=F("project__prj_cd"),
            gr_code=F("gear__gr_code"),
            effcnt=F("gear__effcnt"),
            effdst=F("gear__effdst"),
            gr_des=F("gear__gr_des"),
        )
        .values("prj_cd", "gr_code", "effcnt", "effdst", "gr_des")
        .order_by("prj_cd", "gr_code")
        .distinct("prj_cd", "gr_code")
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
