"""Serializers for models in fn_portal"""

from common.models import Lake
from django.contrib.auth import get_user_model
from fn_portal.models import (
    FNProtocol,
    FN011,
    FN013,
    FN014,
    FN022,
    FN026,
    FN028,
    Gear,
    ProjectGearProcessType,
)
from rest_framework import serializers

from .common_serializers import LakeSerializer, UserSerializer

User = get_user_model()


class FNProtocolSerializer(serializers.ModelSerializer):
    class Meta:
        model = FNProtocol
        lookup_field = "abbrev"
        fields = (
            "abbrev",
            "label",
        )


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


class FN011WizardSerializer(serializers.ModelSerializer):
    """
    A FN011 serializer that will be used exclusivly by our project
    wizard endpoint. This serializer is a simplified version of the
    main FN011 serializer which is used mostly for read-only
    operations and includes nested objects for project lead, protocol
    and lake. This serializer is used to create new FN011 records and
    has uses slugs to identify the related enties.
    """

    lake = serializers.SlugRelatedField(
        queryset=Lake.objects.all(), slug_field="abbrev"
    )
    prj_ldr = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field="username"
    )
    protocol = serializers.SlugRelatedField(
        queryset=FNProtocol.objects.all(), slug_field="abbrev"
    )

    class Meta:
        model = FN011
        lookup_field = "prj_cd"
        fields = (
            "prj_cd",
            "prj_nm",
            "prj_date0",
            "prj_date1",
            "comment0",
            "prj_ldr",
            "protocol",
            "lake",
        )


class ProjectGearProcessTypeSerializer(serializers.ModelSerializer):
    """
    A serializer used by the Project Wizard to create
    Project-Gear-ProcessType entries.  Accepts json object of the form:

    {slug:"lha_ia21_123", gear:"GL50", process_type:"1"}

    """

    project = serializers.SlugRelatedField(
        many=False, queryset=FN011.objects.all(), slug_field="slug"
    )

    gear = serializers.SlugRelatedField(
        many=False, queryset=Gear.objects.all(), slug_field="gr_code"
    )

    class Meta:
        model = ProjectGearProcessType
        fields = ("project", "gear", "process_type")


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
        many=False, queryset=FN011.objects.all(), slug_field="slug"
    )

    class Meta:
        model = FN022
        fields = ("project", "ssn", "ssn_des", "ssn_date0", "ssn_date1", "slug")


class FN026SimpleSerializer(serializers.ModelSerializer):
    """This is a super minimal serializer for spatial strata associated
    with a project. It is used by the FN Project wizard to created named
    strata with a lat-lon, but nothing more.
    """

    project = serializers.SlugRelatedField(
        many=False, queryset=FN011.objects.all(), slug_field="slug"
    )

    class Meta:
        model = FN026
        fields = (
            "project",
            "space",
            "space_des",
            "dd_lat",
            "dd_lon",
        )


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
            "dd_lat",
            "dd_lon",
        )


class FN028SimpleSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        many=False, queryset=FN011.objects.all(), slug_field="slug"
    )
    gear = serializers.SlugRelatedField(
        many=False, queryset=Gear.objects.all(), slug_field="gr_code"
    )

    class Meta:
        model = FN028
        fields = (
            "project",
            "mode",
            "mode_des",
            "gear",
            "gruse",
            "orient",
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
