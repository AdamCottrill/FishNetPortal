import django_filters

from ..models import FN121Weather
from .common_filters import ValueInFilter
from .FN121AttributeFilter import FN121AttributeFilter


class FN121WeatherFilter(FN121AttributeFilter):
    """A filter that is inherited from FN121AttributeFilter and filter
    by additional weather attributes

    """

    airtem0 = django_filters.NumberFilter(field_name="airtem0", lookup_expr="exact")
    airtem0__gte = django_filters.NumberFilter(field_name="airtem0", lookup_expr="gte")
    airtem0__lte = django_filters.NumberFilter(field_name="airtem0", lookup_expr="lte")
    airtem0__gt = django_filters.NumberFilter(field_name="airtem0", lookup_expr="gt")
    airtem0__lt = django_filters.NumberFilter(field_name="airtem0", lookup_expr="lt")
    airtem0__null = django_filters.BooleanFilter(
        field_name="airtem0", lookup_expr="isnull"
    )
    airtem0__not_null = django_filters.BooleanFilter(
        field_name="airtem0", lookup_expr="isnull", exclude=True
    )

    airtem1 = django_filters.NumberFilter(field_name="airtem1", lookup_expr="exact")
    airtem1__gte = django_filters.NumberFilter(field_name="airtem1", lookup_expr="gte")
    airtem1__lte = django_filters.NumberFilter(field_name="airtem1", lookup_expr="lte")
    airtem1__gt = django_filters.NumberFilter(field_name="airtem1", lookup_expr="gt")
    airtem1__lt = django_filters.NumberFilter(field_name="airtem1", lookup_expr="lt")
    airtem1__null = django_filters.BooleanFilter(
        field_name="airtem1", lookup_expr="isnull"
    )
    airtem1__not_null = django_filters.BooleanFilter(
        field_name="airtem1", lookup_expr="isnull", exclude=True
    )

    wind_speed0 = django_filters.NumberFilter(
        field_name="wind_speed0", lookup_expr="exact"
    )
    wind_speed0__gte = django_filters.NumberFilter(
        field_name="wind_speed0", lookup_expr="gte"
    )
    wind_speed0__lte = django_filters.NumberFilter(
        field_name="wind_speed0", lookup_expr="lte"
    )
    wind_speed0__gt = django_filters.NumberFilter(
        field_name="wind_speed0", lookup_expr="gt"
    )
    wind_speed0__lt = django_filters.NumberFilter(
        field_name="wind_speed0", lookup_expr="lt"
    )
    wind_speed0__null = django_filters.BooleanFilter(
        field_name="wind_speed0", lookup_expr="isnull"
    )
    wind_speed0__not_null = django_filters.BooleanFilter(
        field_name="wind_speed0", lookup_expr="isnull", exclude=True
    )

    wind_direction0 = django_filters.NumberFilter(
        field_name="wind_direction0", lookup_expr="exact"
    )
    wind_direction0__gte = django_filters.NumberFilter(
        field_name="wind_direction0", lookup_expr="gte"
    )
    wind_direction0__lte = django_filters.NumberFilter(
        field_name="wind_direction0", lookup_expr="lte"
    )
    wind_direction0__gt = django_filters.NumberFilter(
        field_name="wind_direction0", lookup_expr="gt"
    )
    wind_direction0__lt = django_filters.NumberFilter(
        field_name="wind_direction0", lookup_expr="lt"
    )
    wind_direction0__null = django_filters.BooleanFilter(
        field_name="wind_direction0", lookup_expr="isnull"
    )
    wind_direction0__not_null = django_filters.BooleanFilter(
        field_name="wind_direction0", lookup_expr="isnull", exclude=True
    )

    wind_speed1 = django_filters.NumberFilter(
        field_name="wind_speed1", lookup_expr="exact"
    )
    wind_speed1__gte = django_filters.NumberFilter(
        field_name="wind_speed1", lookup_expr="gte"
    )
    wind_speed1__lte = django_filters.NumberFilter(
        field_name="wind_speed1", lookup_expr="lte"
    )
    wind_speed1__gt = django_filters.NumberFilter(
        field_name="wind_speed1", lookup_expr="gt"
    )
    wind_speed1__lt = django_filters.NumberFilter(
        field_name="wind_speed1", lookup_expr="lt"
    )
    wind_speed1__null = django_filters.BooleanFilter(
        field_name="wind_speed1", lookup_expr="isnull"
    )
    wind_speed1__not_null = django_filters.BooleanFilter(
        field_name="wind_speed1", lookup_expr="isnull", exclude=True
    )

    wind_direction1 = django_filters.NumberFilter(
        field_name="wind_direction1", lookup_expr="exact"
    )
    wind_direction1__gte = django_filters.NumberFilter(
        field_name="wind_direction1", lookup_expr="gte"
    )
    wind_direction1__lte = django_filters.NumberFilter(
        field_name="wind_direction1", lookup_expr="lte"
    )
    wind_direction1__gt = django_filters.NumberFilter(
        field_name="wind_direction1", lookup_expr="gt"
    )
    wind_direction1__lt = django_filters.NumberFilter(
        field_name="wind_direction1", lookup_expr="lt"
    )
    wind_direction1__null = django_filters.BooleanFilter(
        field_name="wind_direction1", lookup_expr="isnull"
    )
    wind_direction1__not_null = django_filters.BooleanFilter(
        field_name="wind_direction1", lookup_expr="isnull", exclude=True
    )

    precip0 = django_filters.NumberFilter(field_name="precip0", lookup_expr="exact")
    precip0__gte = django_filters.NumberFilter(field_name="precip0", lookup_expr="gte")
    precip0__lte = django_filters.NumberFilter(field_name="precip0", lookup_expr="lte")
    precip0__gt = django_filters.NumberFilter(field_name="precip0", lookup_expr="gt")
    precip0__lt = django_filters.NumberFilter(field_name="precip0", lookup_expr="lt")
    precip0__null = django_filters.BooleanFilter(
        field_name="precip0", lookup_expr="isnull"
    )
    precip0__not_null = django_filters.BooleanFilter(
        field_name="precip0", lookup_expr="isnull", exclude=True
    )

    precip1 = django_filters.NumberFilter(field_name="precip1", lookup_expr="exact")
    precip1__gte = django_filters.NumberFilter(field_name="precip1", lookup_expr="gte")
    precip1__lte = django_filters.NumberFilter(field_name="precip1", lookup_expr="lte")
    precip1__gt = django_filters.NumberFilter(field_name="precip1", lookup_expr="gt")
    precip1__lt = django_filters.NumberFilter(field_name="precip1", lookup_expr="lt")
    precip1__null = django_filters.BooleanFilter(
        field_name="precip1", lookup_expr="isnull"
    )
    precip1__not_null = django_filters.BooleanFilter(
        field_name="precip1", lookup_expr="isnull", exclude=True
    )

    cloud_pc0 = django_filters.NumberFilter(field_name="cloud_pc0", lookup_expr="exact")
    cloud_pc0__gte = django_filters.NumberFilter(
        field_name="cloud_pc0", lookup_expr="gte"
    )
    cloud_pc0__lte = django_filters.NumberFilter(
        field_name="cloud_pc0", lookup_expr="lte"
    )
    cloud_pc0__gt = django_filters.NumberFilter(
        field_name="cloud_pc0", lookup_expr="gt"
    )
    cloud_pc0__lt = django_filters.NumberFilter(
        field_name="cloud_pc0", lookup_expr="lt"
    )
    cloud_pc0__null = django_filters.BooleanFilter(
        field_name="cloud_pc0", lookup_expr="isnull"
    )
    cloud_pc0__not_null = django_filters.BooleanFilter(
        field_name="cloud_pc0", lookup_expr="isnull", exclude=True
    )

    cloud_pc1 = django_filters.NumberFilter(field_name="cloud_pc1", lookup_expr="exact")
    cloud_pc1__gte = django_filters.NumberFilter(
        field_name="cloud_pc1", lookup_expr="gte"
    )
    cloud_pc1__lte = django_filters.NumberFilter(
        field_name="cloud_pc1", lookup_expr="lte"
    )
    cloud_pc1__gt = django_filters.NumberFilter(
        field_name="cloud_pc1", lookup_expr="gt"
    )
    cloud_pc1__lt = django_filters.NumberFilter(
        field_name="cloud_pc1", lookup_expr="lt"
    )
    cloud_pc1__null = django_filters.BooleanFilter(
        field_name="cloud_pc1", lookup_expr="isnull"
    )
    cloud_pc1__not_null = django_filters.BooleanFilter(
        field_name="cloud_pc1", lookup_expr="isnull", exclude=True
    )

    waveht0 = django_filters.NumberFilter(field_name="waveht0", lookup_expr="exact")
    waveht0__gte = django_filters.NumberFilter(field_name="waveht0", lookup_expr="gte")
    waveht0__lte = django_filters.NumberFilter(field_name="waveht0", lookup_expr="lte")
    waveht0__gt = django_filters.NumberFilter(field_name="waveht0", lookup_expr="gt")
    waveht0__lt = django_filters.NumberFilter(field_name="waveht0", lookup_expr="lt")
    waveht0__null = django_filters.BooleanFilter(
        field_name="waveht0", lookup_expr="isnull"
    )
    waveht0__not_null = django_filters.BooleanFilter(
        field_name="waveht0", lookup_expr="isnull", exclude=True
    )

    waveht1 = django_filters.NumberFilter(field_name="waveht1", lookup_expr="exact")
    waveht1__gte = django_filters.NumberFilter(field_name="waveht1", lookup_expr="gte")
    waveht1__lte = django_filters.NumberFilter(field_name="waveht1", lookup_expr="lte")
    waveht1__gt = django_filters.NumberFilter(field_name="waveht1", lookup_expr="gt")
    waveht1__lt = django_filters.NumberFilter(field_name="waveht1", lookup_expr="lt")
    waveht1__null = django_filters.BooleanFilter(
        field_name="waveht1", lookup_expr="isnull"
    )
    waveht1__not_null = django_filters.BooleanFilter(
        field_name="waveht1", lookup_expr="isnull", exclude=True
    )

    precip_duration = ValueInFilter(field_name="precip_duration")
    precip_duration__not = ValueInFilter(field_name="precip_duration", exclude=True)
    precip_duration__null = django_filters.BooleanFilter(
        field_name="precip_duration", lookup_expr="isnull"
    )

    wave_duration = ValueInFilter(field_name="wave_duration")
    wave_duration__not = ValueInFilter(field_name="wave_duration", exclude=True)
    wave_duration__null = django_filters.BooleanFilter(
        field_name="wave_duration", lookup_expr="isnull"
    )

    class Meta:
        model = FN121Weather
        fields = [
            "airtem0",
            "airtem1",
            "wind_direction0",
            "wind_speed0",
            "wind_direction1",
            "wind_speed1",
            "precip0",
            "precip1",
            "cloud_pc0",
            "cloud_pc1",
            "waveht0",
            "waveht1",
            "precip_duration",
            "wave_duration",
        ]
