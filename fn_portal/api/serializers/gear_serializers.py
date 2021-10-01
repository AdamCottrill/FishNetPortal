"""Serializers for models from our common application that will be
used in FN_Portal"""

from rest_framework import serializers

from fn_portal.models import Gear, GearEffortProcessType


class ProcessTypeSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()

    class Meta:
        model = GearEffortProcessType
        fields = ("process_type", "label", "eff")

    def get_label(self, obj):
        return obj.get_process_type_display()


class GearSerializer(serializers.ModelSerializer):
    process_types = ProcessTypeSerializer(many=True, read_only=True)

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
            "process_types",
        )
