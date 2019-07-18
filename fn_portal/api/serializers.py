"""Serializers for models in fn_portal"""

from rest_framework import serializers

from fn_portal.models import (
    Species,
    FN011,
    FN121,
    FN122,
    FN123,
    FN125,
    FN125Tag,
    FN125_Lamprey,
    FN126,
    FN127,
)


# Serializers define the API representation.
class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        lookup_field = "species_code"
        fields = ("species_code", "common_name", "scientific_name")


# Serializers define the API representation.
class FN011Serializer(serializers.ModelSerializer):

    protocol = serializers.CharField(read_only=True, source="protocol.abbrev")

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


class FN121Serializer(serializers.ModelSerializer):

    effdt0 = serializers.DateField(format="%Y-%m-%d")
    effdt1 = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = FN121

        # need to get prj_cd from FN011 table.

        fields = (
            "id",
            "slug",
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

    def create(self, validated_data):
        validated_data["project"] = self.context["project"]
        return FN121.objects.create(**validated_data)


class FN122Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN122

        fields = ("id", "slug", "eff", "effdst", "grdep", "grtem0", "grtem1")

    def create(self, validated_data):
        """When we create an effort object, we need to add the associated
        sample (net set)."""

        validated_data["sample"] = self.context["sample"]
        return FN122.objects.create(**validated_data)


class FN123Serializer(serializers.ModelSerializer):

    sam = serializers.CharField(read_only=True, source="effort.sample.sam")
    eff = serializers.CharField(read_only=True, source="effort.eff")

    # species = serializers.CharField(source="species.species_code")
    species = serializers.SlugRelatedField(
        queryset=Species.objects.all(), slug_field="species_code"
    )

    class Meta:
        model = FN123
        fields = (
            "id",
            "slug",
            "sam",
            "eff",
            "species",
            "grp",
            "catcnt",
            "catwt",
            "biocnt",
            "comment",
        )

    def create(self, validated_data):
        """When we create new catch count object, we need to add the associated
        effort (within a net within a project)."""

        validated_data["effort"] = self.context["effort"]
        return FN123.objects.create(**validated_data)


class FN125TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN125Tag
        fields = (
            "id",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "xcwtseq",
            "xtaginckd",
            "xtag_chk",
            "comment_tag",
        )


class FN125LampreySerializer(serializers.ModelSerializer):
    class Meta:
        model = FN125_Lamprey
        fields = (
            "id",
            "lamid",
            "xlam",
            "lamijc",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
        )


class FN126Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN126
        fields = ("id", "food", "taxon", "foodcnt", "comment6")


class FN127Serializer(serializers.ModelSerializer):
    class Meta:
        model = FN127
        fields = (
            "id",
            "ageid",
            "agemt",
            "xagem",
            "agea",
            "preferred",
            "conf",
            "nca",
            "edge",
            "agest",
            "comment7",
        )


class FN125Serializer(serializers.ModelSerializer):

    sam = serializers.CharField(read_only=True, source="catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="catch.species.species_code")
    eff = serializers.CharField(read_only=True, source="catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="catch.grp")

    # child tables
    lamprey_marks = FN125LampreySerializer(many=True, required=False, allow_null=True)
    fishtags = FN125TagSerializer(many=True, required=False, allow_null=True)
    diet_data = FN126Serializer(many=True, required=False, allow_null=True)
    age_estimates = FN127Serializer(many=True, required=False, allow_null=True)

    class Meta:
        model = FN125
        fields = (
            "id",
            "slug",
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
            "fishtags",
            "lamprey_marks",
            "age_estimates",
            "diet_data",
            "comment5",
        )

    def create(self, validated_data):

        fishtags = validated_data.pop("fishtags", None)
        diet_items = validated_data.pop("diet_data", None)
        lamprey_marks = validated_data.pop("lamprey_marks", None)
        age_estimates = validated_data.pop("age_estimates", None)

        validated_data["catch_count"] = self.context["catch_count"]

        fish = FN125.objects.create(**validated_data)

        for fishtag in fishtags:
            FN125Tag.objects.create(fish=fish, **fishtag)

        for item in diet_items:
            FN126.objects.create(fish=fish, **item)

        for estimate in age_estimates:
            FN127.objects.create(fish=fish, **estimate)

        for mark in lamprey_marks:
            FN125_Lamprey.objects.create(fish=fish, **mark)

        return fish


#    def update(self, instance, validated_data):
#         """A custom update method that explicitly updates associated records
#         for tags, age estimates, lamprey wounds, and diet items."""
#
#         instance.flen = (validated_data("flen", instance.flen),)
#         instance.tlen = (validated_data("tlen", instance.tlen),)
#         instance.rwt = (validated_data("rwt", instance.rwt),)
#         instance.girth = (validated_data("girth", instance.girth),)
#         instance.clipc = (validated_data("clipc", instance.clipc),)
#         instance.sex = (validated_data("sex", instance.sex),)
#         instance.mat = (validated_data("mat", instance.mat),)
#         instance.gon = (validated_data("gon", instance.gon),)
#         instance.noda = (validated_data("noda", instance.noda),)
#         instance.nodc = (validated_data("nodc", instance.nodc),)
#         instance.agest = (validated_data("agest", instance.agest),)
#         instance.fate = validated_data("fate", instance.fate)
#         instance.save()
#
#         fishtags = validated_data.pop("fishtags", None)
#         diet_items = validated_data.pop("diet_data", None)
#         lamprey_marks = validated_data.pop("lamprey_marks", None)
#         age_estimates = validated_data.pop("age_estimates", None)
#
#         # fn125 = FN125.objects.create(**validated_data)
#
#         for fishtag in fishtags:
#             fishtag_id = fishtag.get("id", None)
#             if fishtag_id:
#                 obj = FN125Tag.objects.get(id=fishtag_id, fish=instance)
#                 # for each field in our object get the new values or use the old
#                 obj.fish_tag_id = (fishtag.get("fish_tag_id", obj.fish_tag_id),)
#                 obj.tagstat = fishtag.get("tagstat", obj.tagstat)
#                 obj.tagid = fishtag.get("tagid", obj.tagid)
#                 obj.tagdoc = fishtag.get("tagdoc", obj.tagdoc)
#                 obj.xcwtseq = fishtag.get("xcwtseq", obj.xcwtseq)
#                 obj.xtaginckt = fishtag.get("xtaginckd", obj.taginckt)
#                 obj.xtag_chk = fishtag.get("xtag_chk", obj.xtag_chk)
#                 obj.comment_tag = fishtag.get("comment_tag", obj.comment_tag)
#                 obj.save()
#             else:
#                 FN125Tag.objects.create(fish=instance, **fishtag)
#
#         for item in diet_items:
#             item_id = item.get("id", None)
#             if item_id:
#                 obj = FN126.objects.get(id=item_id, fish=instance)
#                 # for each field in our object get the new values or use the old
#                 obj.food = item.get("food", obj.food)
#                 obj.taxon = item.get("taxon", obj.taxon)
#                 obj.foodcnt = item.get("foodcnt", obj.foodcnt)
#                 obj.comment6 = item.get("comment6", obj.comment6)
#                 obj.save()
#             else:
#                 FN126.objects.create(fish=instance, **item)
#
#         for estimate in age_estimates:
#             estimate_id = estimate.get("id", None)
#             if estimate_id:
#                 obj = FN127.objects.get(id=estimate_id, fish=instance)
#                 # for each field in our object get the new values or use the old
#                 obj.agea = estimate.get("agea", obj.agea)
#                 obj.preferred = estimate.get("preferred", obj.preferred)
#                 obj.agest = estimate.get("agest", obj.agest)
#                 obj.xagem = estimate.get("xagem", obj.xagem)
#                 obj.agemt = estimate.get("agemt", obj.agemt)
#                 obj.edge = estimate.get("edge", obj.edge)
#                 obj.conf = estimate.get("conf", obj.conf)
#                 obj.nca = estimate.get("nca", obj.nca)
#                 obj.comment7 = estimate.get("comment7", obj.comment7)
#                 obj.save()
#             else:
#                 FN127.objects.create(fish=instance, **estimate)
#
#         for mark in lamprey_marks:
#             mark_id = mark.get("id", None)
#             if mark_id:
#                 obj = FN125_Lamprey.objects.get(id=mark_id, fish=instance)
#                 # for each field in our object get the new values or use the old
#                 obj.lamid = mark.get("lamid", obj.lamid)
#                 obj.xlam = mark.get("xlam", obj.xlam)
#                 obj.lamijc = mark.get("lamijc", obj.lamijc)
#                 obj.lamijc_type = mark.get("lamijc_type", obj.lamijc_type)
#                 obj.lamijc_size = mark.get("lamijc_size", obj.lamijc_size)
#                 obj.comment_lam = mark.get("comment_lam", obj.comment_lam)
#                 obj.save()
#             else:
#                 FN125_Lamprey.objects.create(fish=instance, **mark)
#
#         return instance
