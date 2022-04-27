"""Views for api endpoints for our FN0 models."""
import csv

from rest_framework import generics
from django.db.models import F, Value
from django.db.models.functions import Concat, LPad
from django.http import HttpResponse

from fn_portal.models import (
    FNProtocol,
    FN011,
    FN012,
    FN012Protocol,
    FN013,
    FN014,
    FN022,
    FN026,
    FN028,
    Gear,
)

from ...filters import (
    FN011Filter,
    FN012Filter,
    FN012ProtocolFilter,
    FN022Filter,
    FN026Filter,
    FN028Filter,
)

from ..utils import StandardResultsSetPagination

from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly, ReadOnly
from ..serializers import (
    FNProtocolSerializer,
    FN011Serializer,
    FN012ListSerializer,
    FN012ProtocolListSerializer,
    FN013Serializer,
    FN013ListSerializer,
    FN014Serializer,
    FN022Serializer,
    FN022ListSerializer,
    FN026Serializer,
    FN026ListSerializer,
    FN028Serializer,
    FN028ListSerializer,
)


class FNProtocolListView(generics.ListAPIView):
    """A read-only endpoint to return currently available protocols."""

    serializer_class = FNProtocolSerializer
    permission_classes = [ReadOnly]
    pagination_class = None

    def get_queryset(self):
        """by default, we only want to return active protocols
        that has been documented. If 'all' is specified, we return
        everything.

        Boolean confirmed arguments for active and confirmed allow us
        to refine which subsets are returned.

        """

        all = self.request.query_params.get("all", False)
        confirmed = self.request.query_params.get("confirmed")
        active = self.request.query_params.get("active")

        queryset = FNProtocol.objects.order_by("abbrev").all()

        if bool(all):
            return queryset
        else:
            if confirmed is None:
                queryset = queryset.filter(confirmed=True)
            else:
                confirmed = confirmed.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(confirmed=confirmed)

            if active is None:
                queryset = queryset.filter(active=True)
            else:
                active = active.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(active=active)

        return queryset


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
    )


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
        .order_by("slug")
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


class FN022ListView(generics.ListAPIView):
    """an api end point to list all of the seasons (FN022) associated with a
    project."""

    serializer_class = FN022ListSerializer
    filterset_class = FN022Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd")
        qs = FN022.objects.all().select_related("project")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs


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

    serializer_class = FN026ListSerializer
    filterset_class = FN026Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""

        qs = FN026.objects.all().select_related("project")
        prj_cd = self.kwargs.get("prj_cd")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs


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

    serializer_class = FN028ListSerializer
    filterset_class = FN028Filter
    pagination_class = StandardResultsSetPagination
    permission_classes = [ReadOnly]

    def get_queryset(self):
        """"""

        return FN028.objects.all().select_related("project", "gear")


class FN028DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An api endpoint for get, put and delete endpoints for fishing mode
    objects associated with a specfic project.

    """

    lookup_field = "mode"
    serializer_class = FN028Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""

        qs = FN028.objects.all().select_related("project", "gear")
        prj_cd = self.kwargs.get("prj_cd")
        if prj_cd:
            qs = qs.filter(project__slug=prj_cd.lower())
        return qs
