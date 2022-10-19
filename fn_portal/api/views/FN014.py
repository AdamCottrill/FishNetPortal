"""Views for api endpoints for our FN0 models."""


from fn_portal.models import FN014
from rest_framework import generics


from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import FN014Serializer


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
