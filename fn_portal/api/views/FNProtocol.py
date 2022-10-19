"""Views for api endpoints for our FN Protocol models."""


from fn_portal.models import FNProtocol

from rest_framework import generics

from ..permissions import ReadOnly
from ..serializers import FNProtocolSerializer


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
