"""Views for gear api endpoints - gear, sub-gearsm, and process types,."""

import operator
from functools import reduce
from django.db.models import Q
from fn_portal.models import Gear, GearEffortProcessType, ProjectGearProcessType
from rest_framework import generics

from ...filters import GearEffortProcessTypeFilter, GearFilter
from ..permissions import ReadOnly
from ..serializers import GearEffortProcessTypeSerializer, GearSerializer


class GearEffortProcessTypeListView(generics.ListAPIView):
    """a simple, read only list view to return all of gear-effort-process
    types from our database.  Accepts filters for gear type, gear code
    'like', gear code, and process type in. as well as boolean flags
    for 'confirmed' and 'depreciated'. By default only process types that
    are associated wiht confirmed, active gears are returne. Other are
    available on request.

    """

    pagination_class = None
    serializer_class = GearEffortProcessTypeSerializer
    permission_classes = [ReadOnly]
    filterset_class = GearEffortProcessTypeFilter

    def get_queryset(self):
        """by default, we only want to return active (non-deprecated) gear
        that has been documented. If 'all' is specified, we return
        everything.

        If confirmed is false - all gear, otherwise only confirmed
        gear by default

        if depreciated is true - return only depreciated gears,
        otherwise return those that are not depreciated (actively in
        use).

        """
        all = self.request.query_params.get("all", False)
        confirmed = self.request.query_params.get("confirmed")
        depreciated = self.request.query_params.get("depreciated")

        queryset = GearEffortProcessType.objects.all().select_related("gear")

        if bool(all):
            return queryset
        else:
            if confirmed is None:
                queryset = queryset.filter(gear__confirmed=True)
            else:
                confirmed = confirmed.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(gear__confirmed=confirmed)

            if depreciated is None:
                queryset = queryset.filter(gear__depreciated=False)
            else:
                depreciated = depreciated.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(gear__depreciated=depreciated)
        return queryset


class ProjectGearEffortProcessTypeListView(generics.ListAPIView):
    """
    The ProjectGearEffortProcessTypeList endpoint should return a
    list of the gears, process types, and efforts for each gear type
    associated with a single project.

    """

    pagination_class = None
    serializer_class = GearEffortProcessTypeSerializer
    permission_classes = [ReadOnly]
    filterset_class = GearEffortProcessTypeFilter

    def get_queryset(self):
        """Given our project code, fetch gear and process types for that project
        and use those to filter the gear effort process types
        associated with each of them."""

        project_slug = self.kwargs.get("slug")

        gear_process_types = ProjectGearProcessType.objects.filter(
            project__slug=project_slug
        )

        filter_list = []
        for gpt in gear_process_types:
            # qs = qs.filter(Q(gear=gpt.gear) & Q(process_type=gpt.process_type))
            filter_list.append(Q(gear=gpt.gear) & Q(process_type=gpt.process_type))

        qs = GearEffortProcessType.objects.select_related("gear").filter(
            reduce(operator.or_, filter_list)
        )

        return qs


class GearListView(generics.ListAPIView):
    """a simple, read only list view to return all of gear types from our
    database.  Accepts filters for gear type,
    active/documented/depreciated, gear code 'like', and gear code
    in. Returns basic gear attrbiutes (and someday - known/approved process types).

    """

    pagination_class = None
    serializer_class = GearSerializer
    permission_classes = [ReadOnly]
    filterset_class = GearFilter

    def get_queryset(self):
        """by default, we only want to return active (non-deprecated) gear
        that has been documented. If 'all' is specified, we return
        everything.

        If confirmed is false - all gear, otherwise only confirmed
        gear by default

        if depreciated is true - return only depreciated gears,
        otherwise return those that are not depreciated (actively in
        use).

        """
        all = self.request.query_params.get("all", False)
        confirmed = self.request.query_params.get("confirmed")
        depreciated = self.request.query_params.get("depreciated")

        queryset = Gear.objects.prefetch_related("process_types").all()

        if bool(all):
            return queryset
        else:
            if confirmed is None:
                queryset = queryset.filter(confirmed=True)
            else:
                confirmed = confirmed.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(confirmed=confirmed)

            if depreciated is None:
                queryset = queryset.filter(depreciated=False)
            else:
                depreciated = depreciated.lower() in ("yes", "true", "t", "1")
                queryset = queryset.filter(depreciated=depreciated)

        return queryset
