import django_filters

from ..models import FN121ElectroFishing

from .FN121AttributeFilter import FN121AttributeFilter
from .common_filters import ValueInFilter


class FN121ElectroFishingFilter(FN121AttributeFilter):
    """A filter that is inherited from FN121AttributeFilter and filter
    by additional ElectroFishing attributes

    """

    shock_sec = django_filters.NumberFilter(field_name="shock_sec", lookup_expr="exact")
    shock_sec__gte = django_filters.NumberFilter(
        field_name="shock_sec", lookup_expr="gte"
    )
    shock_sec__lte = django_filters.NumberFilter(
        field_name="shock_sec", lookup_expr="lte"
    )
    shock_sec__gt = django_filters.NumberFilter(
        field_name="shock_sec", lookup_expr="gt"
    )
    shock_sec__lt = django_filters.NumberFilter(
        field_name="shock_sec", lookup_expr="lt"
    )
    shock_sec__null = django_filters.BooleanFilter(
        field_name="shock_sec", lookup_expr="isnull"
    )
    shock_sec__not_null = django_filters.BooleanFilter(
        field_name="shock_sec", lookup_expr="isnull", exclude=True
    )

    volts_mean = django_filters.NumberFilter(
        field_name="volts_mean", lookup_expr="exact"
    )
    volts_mean__gte = django_filters.NumberFilter(
        field_name="volts_mean", lookup_expr="gte"
    )
    volts_mean__lte = django_filters.NumberFilter(
        field_name="volts_mean", lookup_expr="lte"
    )
    volts_mean__gt = django_filters.NumberFilter(
        field_name="volts_mean", lookup_expr="gt"
    )
    volts_mean__lt = django_filters.NumberFilter(
        field_name="volts_mean", lookup_expr="lt"
    )
    volts_mean__null = django_filters.BooleanFilter(
        field_name="volts_mean", lookup_expr="isnull"
    )
    volts_mean__not_null = django_filters.BooleanFilter(
        field_name="volts_mean", lookup_expr="isnull", exclude=True
    )

    amps_mean = django_filters.NumberFilter(field_name="amps_mean", lookup_expr="exact")
    amps_mean__gte = django_filters.NumberFilter(
        field_name="amps_mean", lookup_expr="gte"
    )
    amps_mean__lte = django_filters.NumberFilter(
        field_name="amps_mean", lookup_expr="lte"
    )
    amps_mean__gt = django_filters.NumberFilter(
        field_name="amps_mean", lookup_expr="gt"
    )
    amps_mean__lt = django_filters.NumberFilter(
        field_name="amps_mean", lookup_expr="lt"
    )
    amps_mean__null = django_filters.BooleanFilter(
        field_name="amps_mean", lookup_expr="isnull"
    )
    amps_mean__not_null = django_filters.BooleanFilter(
        field_name="amps_mean", lookup_expr="isnull", exclude=True
    )

    power_mean = django_filters.NumberFilter(
        field_name="power_mean", lookup_expr="exact"
    )
    power_mean__gte = django_filters.NumberFilter(
        field_name="power_mean", lookup_expr="gte"
    )
    power_mean__lte = django_filters.NumberFilter(
        field_name="power_mean", lookup_expr="lte"
    )
    power_mean__gt = django_filters.NumberFilter(
        field_name="power_mean", lookup_expr="gt"
    )
    power_mean__lt = django_filters.NumberFilter(
        field_name="power_mean", lookup_expr="lt"
    )
    power_mean__null = django_filters.BooleanFilter(
        field_name="power_mean", lookup_expr="isnull"
    )
    power_mean__not_null = django_filters.BooleanFilter(
        field_name="power_mean", lookup_expr="isnull", exclude=True
    )

    waveform = ValueInFilter(field_name="waveform")
    waveform__not = ValueInFilter(field_name="waveform", exclude=True)
    waveform__null = django_filters.BooleanFilter(
        field_name="waveform", lookup_expr="isnull"
    )
    waveform__not_null = django_filters.BooleanFilter(
        field_name="wavefrom", lookup_expr="isnull", exclude=True
    )

    class Meta:
        model = FN121ElectroFishing
        fields = [
            "shock_sec",
            "volts_mean",
            "amps_mean",
            "power_mean",
            "waveform",
        ]
