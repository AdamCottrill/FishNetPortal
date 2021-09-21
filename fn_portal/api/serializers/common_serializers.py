"""Serializers for models from our common application that will be
used in FN_Portal"""

from fn_portal.data_upload.project_upload import process_accdb_upload
from rest_framework import serializers
from django.contrib.auth import get_user_model
from common.models import Lake, Species, Grid5

User = get_user_model()


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        lookup_field = "spc"
        fields = ("spc", "spc_nmco", "spc_nmsc")


class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid5
        lookup_field = "slug"
        fields = ("slug", "grid")
        read_only_fields = ("slug",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        lookup_field = "username"
        fields = ("username", "first_name", "last_name")


class LakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lake
        lookup_field = "abbrev"
        fields = ("lake_name", "abbrev")


class LakeExtentSerializer(serializers.ModelSerializer):
    """
    A serializer for lake objects that returns the lake name, lake
    abbreviation, and the extent of the ontario waters of the lake.

    """

    extent = serializers.SerializerMethodField()

    class Meta:
        model = Lake
        lookup_field = "abbrev"
        fields = ("lake_name", "abbrev", "extent")

    def get_extent(self, obj):
        """
        return the envelope encapsulating the ontario waters of the lake in question.

        Arguments:
        - `self`:
        - `obj`:
        """

        return obj.geom_ontario.extent
