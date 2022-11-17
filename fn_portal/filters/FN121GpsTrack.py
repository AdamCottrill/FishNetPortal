import django_filters

from ..models import FN121GpsTrack

from .common_filters import GeomFilter

from .FN121AttributeFilter import FN121AttributeFilter


class FN121GpsTrackFilter(FN121AttributeFilter):
    """A filter that is inherited from FN122SubFilter and allows
    additional filters based on attributes of the gps track point
    itself.

    """

    track_sidep = django_filters.NumberFilter(field_name="sidep", lookup_expr="exact")
    track_sidep__gte = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="gte"
    )
    track_sidep__lte = django_filters.NumberFilter(
        field_name="sidep", lookup_expr="lte"
    )
    track_sidep__gt = django_filters.NumberFilter(field_name="sidep", lookup_expr="gt")
    track_sidep__lt = django_filters.NumberFilter(field_name="sidep", lookup_expr="lt")

    # allow us to filter by and between dates using one or both of:
    # timestamp_date_before and timestamp_date_after
    # ignores the time:
    timestamp_date = django_filters.DateFromToRangeFilter()

    timestamp__gte = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    timestamp__lte = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lte"
    )
    timestamp__gt = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gt"
    )
    timestamp__lt = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lt"
    )

    # these will be applied to the geom of track record:
    track_roi = GeomFilter(field_name="geom__within", method="filter_roi")
    track_buffered_point = GeomFilter(field_name="geom__within", method="filter_point")

    class Meta:
        model = FN121GpsTrack
        fields = ["sidep", "timestamp"]
