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


class GearEffortProcessTypeSerializer(serializers.ModelSerializer):
    """A readonly serializer that returns the gear, effort, process type,
    and grlen avaialble for each gear.  This serializer and associated
    end point will be used to populate template databases by some of
    our data adapter tools.
    """

    gr = serializers.CharField(source="gear.gr_code")

    class Meta:
        model = GearEffortProcessType
        fields = ("gr", "process_type", "eff", "effdst")
