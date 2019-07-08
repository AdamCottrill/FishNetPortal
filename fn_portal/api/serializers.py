"""Serializers for models in fn_portal"""

from rest_framework import serializers

from fn_portal.models import FN011, FN121


# Serializers define the API representation.
class FN011Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FN011
        lookup_field = "prj_cd"
        fields = (
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


class FN121Serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FN121

        # need to get prj_cd from FN011 table.

        fields = (
            "sam ",
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
            "dd_lat ",
            "dd_lon",
            "sitem",
            "comment1",
            "secchi",
        )
