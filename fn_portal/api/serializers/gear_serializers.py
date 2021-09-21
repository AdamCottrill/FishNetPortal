"""Serializers for models from our common application that will be
used in FN_Portal"""

from rest_framework import serializers

from fn_portal.models import Gear


class GearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gear
        lookup_field = "gr_code"

        fields = (
            "gr_label",
            "grtp",
            "gr_code",
            "effcnt",
            "effdst",
            "gr_des",
            "confirmed",
            "depreciated",
        )
