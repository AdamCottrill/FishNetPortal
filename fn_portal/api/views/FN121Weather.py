"""Views for api endpoints."""

from django.db.models import F, CharField, Value, Case, When, Q
from django.db.models.functions import Concat
from fn_portal.models import FN121Weather
from rest_framework import generics

from ...filters import FN121WeatherFilter
from ..serializers import FN121WeatherReadOnlySerializer
from ..utils import LargeResultsSetPagination


class FN121WeatherList(generics.ListAPIView):
    """A read-only endpoint for Weather data.  Accepts all of the query
    parmeters as FN121, with addition of 'gte', 'gt', 'lt', 'lte',
    'null' and 'not_null' arguments for each limnologilal parameter.
    """

    serializer_class = FN121WeatherReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121WeatherFilter

    queryset = (
        FN121Weather.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(
            prj_cd=F("sample__project__prj_cd"),
            sam=F("sample__sam"),
            xweather=Concat(
                "precip_duration", "wave_duration", output_field=CharField()
            ),
            wind0=Case(
                When(Q(wind_speed0="0") & Q(wind_direction0="0"), then=Value("000")),
                When(
                    Q(wind_speed0__isnull=False) & Q(wind_direction0__isnull=False),
                    then=Concat(
                        "wind_direction0",
                        Value("-"),
                        "wind_speed0",
                        output_field=CharField(),
                    ),
                ),
                default=Value(""),
            ),
            wind1=Case(
                When(Q(wind_speed1="0") & Q(wind_direction1="0"), then=Value("000")),
                When(
                    Q(wind_speed1__isnull=False) & Q(wind_direction1__isnull=False),
                    then=Concat(
                        "wind_direction1",
                        Value("-"),
                        "wind_speed1",
                        output_field=CharField(),
                    ),
                ),
                default=Value(""),
            ),
        )
        .values(
            "prj_cd",
            "sam",
            "airtem0",
            "airtem1",
            "wind0",
            "wind1",
            "precip0",
            "precip1",
            "cloud_pc0",
            "cloud_pc1",
            "waveht0",
            "waveht1",
            "xweather",
            "slug",
        )
    )
