"""Serializers for models in fn_portal"""

from fn_portal.models import FN011, FN013, FN014, FN022, FN026, FN028
from rest_framework import serializers

from .common_serializers import LakeSerializer, UserSerializer


class FN011SimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN011
        lookup_field = "prj_cd"
        fields = (
            "prj_cd",
            "prj_nm",
        )


# Serializers define the API representation.
class FN011Serializer(serializers.ModelSerializer):

    protocol = serializers.CharField(read_only=True, source="protocol.abbrev")
    lake = LakeSerializer(many=False)
    prj_ldr = UserSerializer(many=False)

    class Meta:
        model = FN011
        lookup_field = "prj_cd"
        fields = (
            "id",
            "year",
            "prj_cd",
            "slug",
            "prj_nm",
            "prj_ldr",
            "prj_date0",
            "prj_date1",
            "protocol",
            "source",
            "lake",
            "comment0",
        )


class FN013Serializer(serializers.ModelSerializer):
    """Class to serialize the FN013 (gears) used in each project."""

    project = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="slug"
    )

    class Meta:
        model = FN013
        fields = ("project", "gr", "effcnt", "effdst", "gr_des", "slug")


class FN014Serializer(serializers.ModelSerializer):
    """Class to serialize the FN014 (gear/panel detail) used in each project."""

    gear = serializers.SlugRelatedField(many=False, read_only=True, slug_field="slug")

    class Meta:
        model = FN014
        fields = (
            "gear",
            "eff",
            "mesh",
            "grlen",
            "grht",
            "grwid",
            "grcol",
            "grmat",
            "gryarn",
            "grknot",
            "eff_des",
            "slug",
        )


class FN022Serializer(serializers.ModelSerializer):
    """Class to serialize the seasons (temporal strata) used in each project."""

    project = serializers.SlugRelatedField(
        many=False, read_only=True, slug_field="slug"
    )

    class Meta:
        model = FN022
        fields = ("project", "ssn", "ssn_des", "ssn_date0", "ssn_date1", "slug")


class FN026Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN026
        fields = (
            "project",
            "label",
            "space",
            "space_des",
            "area_lst",
            "grdep_ge",
            "grdep_lt",
            "sidep_ge",
            "sidep_lt",
            "grid_ge",
            "grid_lt",
            "site_lst",
            "sitp_lst",
            "ddlat",
            "ddlon",
        )


class FN028Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN028
        fields = (
            "project",
            "mode",
            "mode_des",
            "gear",
            "gruse",
            "orient",
            "effdur_ge",
            "effdur_lt",
            "efftm0_ge",
            "efftm0_lt",
            "slug",
        )
