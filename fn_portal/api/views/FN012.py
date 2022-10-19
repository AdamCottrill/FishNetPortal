"""Views for api endpoints for our FN0 models."""
import csv

from django.db.models import F, Value
from django.db.models.functions import Concat, LPad
from django.http import HttpResponse
from fn_portal.models import FN012, FN012Protocol
from rest_framework import generics

from ...filters import FN012Filter, FN012ProtocolFilter
from ..permissions import ReadOnly
from ..serializers import FN012ListSerializer, FN012ProtocolListSerializer
from ..utils import StandardResultsSetPagination


class FN012ListView(generics.ListAPIView):
    """An api end point to list all of the sampling specs (species and
    group) for a specific project."""

    serializer_class = FN012ListSerializer
    filterset_class = FN012Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]
    queryset = (
        FN012.objects.all()
        .select_related("project", "species")
        .order_by("species", "grp")
    )


class FN012ProtocolListView(generics.ListAPIView):
    """An api end point to list all of the sampling specs (species and
    group) for a specific lake and protocol."""

    serializer_class = FN012ProtocolListSerializer
    filterset_class = FN012ProtocolFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """ """
        qs = (
            FN012Protocol.objects.select_related("protocol", "species")
            .prefetch_related("lake")
            .order_by("slug")
            .all()
        )
        return qs

    def get(self, request, *args, **kwargs):
        """ """
        default = super(FN012ProtocolListView, self).get(request, *args, **kwargs)
        if request.GET.get("export") == "csv":
            return self.export(request, *args, **kwargs)
        return default

    def export(self, request, *args, **kwargs):

        lake = request.GET.get("lake")
        protocol = request.GET.get("protocol")
        qs = self.get_queryset()

        fields = [
            "spc_nmco",
            "spc",
            "grp",
            "grp_des",
            "biosam",
            "sizsam",
            "sizatt",
            "sizint",
            "fdsam",
            "spcmrk",
            "agedec",
            "agest",
            "lamsam",
            "flen_min",
            "flen_max",
            "tlen_min",
            "tlen_max",
            "rwt_min",
            "rwt_max",
            "k_min_error",
            "k_min_warn",
            "k_max_error",
            "k_max_warn",
        ]

        qs = (
            qs.filter(lake__abbrev=lake, protocol__abbrev=protocol)
            .annotate(
                spc_nmco=F("species__spc_nmco"),
                spc=LPad("species__spc", 3, Value("0")),
                fdsam=Concat("fdsam1", "fdsam2"),
                agedec=Concat("agedec1", "agedec2"),
                spcmrk=Concat("spcmrk1", "spcmrk2"),
            )
            .values_list(*fields)
        )

        filename = f"FN012_Values_{lake}_{protocol}.csv"

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={filename}"

        writer = csv.writer(response)
        writer.writerow(fields)
        writer.writerows(qs)

        return response
