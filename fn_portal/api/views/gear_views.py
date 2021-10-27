"""Views for gear api endpoints - gear, sub-gearsm, and process types,."""

from rest_framework import generics
from fn_portal.models import Gear, GearEffortProcessType

from ...filters import GearFilter, GearEffortProcessTypeFilter
from ..permissions import ReadOnly
from ..serializers import GearSerializer, GearEffortProcessTypeSerializer


class GearEffortProcessTypeListView(generics.ListAPIView):
    """a simple, read only list view to return all of gear-effort-process types from our
    database.  Accepts filters for gear type, gear code 'like', gear code, and process type
    in.

    """

    pagination_class = None
    serializer_class = GearEffortProcessTypeSerializer
    permission_classes = [ReadOnly]
    filterset_class = GearEffortProcessTypeFilter
    queryset = GearEffortProcessType.objects.all().select_related("gear")


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
