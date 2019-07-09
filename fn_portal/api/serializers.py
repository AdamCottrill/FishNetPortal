"""Serializers for models in fn_portal"""

from rest_framework import serializers

from fn_portal.models import FN011, FN121, FN122, FN123, FN125, FN_Tags


# Serializers define the API representation.
class FN011Serializer(serializers.ModelSerializer):
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
            "source",
            "lake",
            "comment0",
        )


class FN121Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN121

        # need to get prj_cd from FN011 table.

        fields = (
            "id",
            "sam",
            "effdt0",
            "effdt1",
            "effdur",
            "efftm0",
            "efftm1",
            "effst",
            "grtp",
            "gr",
            "orient",
            "sidep",
            "site",
            "grid",
            "dd_lat",
            "dd_lon",
            "sitem",
            "comment1",
            "secchi",
        )


class FN122Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN122

        fields = ("id", "eff", "effdst", "grdep", "grtem0", "grtem1")


class FN123Serializer(serializers.ModelSerializer):

    sam = serializers.CharField(read_only=True, source="effort.sample.sam")
    species = serializers.CharField(read_only=True, source="species.species_code")
    eff = serializers.CharField(read_only=True, source="effort.eff")

    class Meta:
        model = FN123
        fields = (
            "id",
            "sam",
            "eff",
            "species",
            "grp",
            "catcnt",
            "catwt",
            "biocnt",
            "comment",
        )


class FN125TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN_Tags
        fields = (
            id,
            # fish_tag_id,
            "tagstat",
            "tagid",
            "tagdoc",
            "xcwtseq",
            "xtaginckd",
            "xtag_chk",
            # comment_tag,
        )


class FN125Serializer(serializers.ModelSerializer):

    sam = serializers.CharField(read_only=True, source="catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="catch.species.species_code")
    eff = serializers.CharField(read_only=True, source="catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="catch.grp")

    tags = FN125TagSerializer(many=True, read_only=True)

    class Meta:
        model = FN125
        fields = (
            "id",
            "sam",
            "species",
            "eff",
            "grp",
            "fish",
            "flen",
            "tlen",
            "rwt",
            "girth",
            "clipc",
            "sex",
            "mat",
            "gon",
            "noda",
            "nodc",
            "agest",
            "fate",
            "tags",
            "comment5",
        )
