"""Serializers for models in fn_portal"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from common.models import Lake, Species, Grid5

from fn_portal.models import (
    FN011,
    FN022,
    FN026,
    FN028,
    FN121,
    FN122,
    FN123,
    FN125,
    FN125Tag,
    FN125_Lamprey,
    FN126,
    FN127,
)

User = get_user_model()

# Serializers define the API representation.
class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Species
        lookup_field = "spc"
        fields = ("spc", "spc_nmco", "spc_nmsc")


# Serializers define the API representation.
class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid5
        lookup_field = "slug"
        fields = ("slug", "grid")
        read_only_fields = ("slug",)


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        lookup_field = "username"
        fields = ("username", "first_name", "last_name")


# Serializers define the API representation.
class LakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lake
        lookup_field = "abbrev"
        fields = ("lake_name", "abbrev")


class SimpleFN011Serializer(serializers.ModelSerializer):
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
            "space_siz",
            "area_lst",
            "aru",
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
            "gr",
            "gruse",
            "orient",
            "effdur_ge",
            "effdur_lt",
            "efftm0_ge",
            "efftm0_lt",
            "slug",
        )


class FN121Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(source="project.prj_cd")
    effdt0 = serializers.DateField(format="%Y-%m-%d")
    effdt1 = serializers.DateField(format="%Y-%m-%d")
    grid = GridSerializer(many=False)

    class Meta:
        model = FN121
        lookup_field = "slug"
        # need to get prj_cd from FN011 table.

        fields = (
            "id",
            "prj_cd",
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
            "slug",
        )

        read_only_fields = ("slug", "id")

    def create(self, validated_data):
        """Custom create method to handle grid - nested serializer."""
        project = self.context["project"]
        validated_data["project"] = project

        grid_data = validated_data.pop("grid")
        validated_data["grid"] = Grid5.objects.get(
            lake=project.lake, grid=grid_data["grid"]
        )

        instance = FN121.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        """We need a custom update method to handle grid"""

        grid_no = validated_data["grid"].get("grid")
        if grid_no != instance.grid.grid:
            grid = Grid5.objects.get(lake=instance.grid.lake, grid=grid_no)
            instance.grid = grid

        instance.sam = validated_data.get("sam", instance.sam)
        instance.effdt0 = validated_data.get("effdt0", instance.effdt0)
        instance.effdt1 = validated_data.get("effdt1", instance.effdt1)
        instance.effdur = validated_data.get("effdur", instance.effdur)
        instance.efftm0 = validated_data.get("efftm0", instance.efftm0)
        instance.efftm1 = validated_data.get("efftm1", instance.efftm1)
        instance.effst = validated_data.get("effst", instance.effst)
        instance.grtp = validated_data.get("grtp", instance.grtp)
        instance.gr = validated_data.get("gr", instance.gr)
        instance.orient = validated_data.get("orient", instance.orient)
        instance.sidep = validated_data.get("sidep", instance.sidep)
        instance.site = validated_data.get("site", instance.site)
        instance.dd_lat = validated_data.get("dd_lat", instance.dd_lat)
        instance.dd_lon = validated_data.get("dd_lon", instance.dd_lon)
        instance.sitem = validated_data.get("sitem", instance.sitem)
        instance.comment = validated_data.get("comment1", instance.comment1)
        instance.secchi = validated_data.get("secchi", instance.secchi)

        instance.save()

        return instance


class FN122Serializer(serializers.ModelSerializer):
    """"""
    prj_cd = serializers.CharField(read_only=True, source="effort.sample.project.prj_cd")
    sam = serializers.CharField(read_only=True, source="effort.sample.sam")
    eff = serializers.CharField(read_only=True, source="effort.eff")

    class Meta:
        model = FN122

        fields = ("id", "prj", "sam", "eff", "effdst", "grdep", "grtem0", "grtem1", "slug",)

    def create(self, validated_data):
        """When we create an effort object, we need to add the associated
        sample (net set)."""

        validated_data["sample"] = self.context["sample"]
        return FN122.objects.create(**validated_data)


class FN123Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(source="effort.sample.project.prj_cd")
    sam = serializers.CharField(read_only=True, source="effort.sample.sam")
    eff = serializers.CharField(read_only=True, source="effort.eff")


    spc = serializers.CharField(source="species.spc")
    # species = serializers.SlugRelatedField(
    #     queryset=Species.objects.all(), slug_field="spc"
    # )

    # spc = SpeciesSerializer(many=False)

    class Meta:
        model = FN123
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "catcnt",
            "catwt",
            "biocnt",
            "comment",
            "slug",
        )

    def create(self, validated_data):
        """When we create new catch count object, we need to add the associated
        effort (within a net within a project)."""

        validated_data["effort"] = self.context["effort"]
        return FN123.objects.create(**validated_data)


class FN125TagNestedSerializer(serializers.ModelSerializer):
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


class FN125LampreyNestedSerializer(serializers.ModelSerializer):
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


class FN126NestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN126
        fields = ("id", "food", "taxon", "foodcnt", "comment6")


class FN127NestedSerializer(serializers.ModelSerializer):
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

    prj_cd = serializers.CharField(
        read_only=True, source="catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="catch.species.spc")
    eff = serializers.CharField(read_only=True, source="catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="catch.grp")

    # child tables
    lamprey_marks = FN125LampreyNestedSerializer(many=True, required=False, allow_null=True)
    fishtags = FN125TagNestedSerializer(many=True, required=False, allow_null=True)
    diet_data = FN126NestedSerializer(many=True, required=False, allow_null=True)
    age_estimates = FN127NestedSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = FN125
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "species",
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
            "slug",
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


class FN125TagSerializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(
        read_only=True, source="fish.catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="fish.catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="fish.catch.species.spc")
    eff = serializers.CharField(read_only=True, source="fish.catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="fish.catch.grp")
    fish = serializers.CharField(read_only=True, source="fish.catch.grp")

    class Meta:
        model = FN125Tag
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "species",
            "grp",
            "fish",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "xcwtseq",
            "xtaginckd",
            "xtag_chk",
            "comment_tag",
            "slug"
        )


class FN125LampreySerializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(
        read_only=True, source="fish.catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="fish.catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="fish.catch.species.spc")
    eff = serializers.CharField(read_only=True, source="fish.catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="fish.catch.grp")
    fish = serializers.CharField(read_only=True, source="fish.catch.grp")

    class Meta:
        model = FN125_Lamprey
        fields = (
            "prj_cd",
            "sam",
            "eff",
            "species",
            "grp",
            "fish",
            "id",
            "lamid",
            "xlam",
            "lamijc",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
            "slug"
        )


class FN126Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(
        read_only=True, source="fish.catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="fish.catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="fish.catch.species.spc")
    eff = serializers.CharField(read_only=True, source="fish.catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="fish.catch.grp")
    fish = serializers.CharField(read_only=True, source="fish.catch.grp")


    class Meta:
        model = FN126
        fields = ("id",
            "prj_cd",
            "sam",
            "eff",
            "species",
            "grp",
            "fish",
                  "food", "taxon", "foodcnt", "comment6", "slug")


class FN127Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(
        read_only=True, source="fish.catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="fish.catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="fish.catch.species.spc")
    eff = serializers.CharField(read_only=True, source="fish.catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="fish.catch.grp")
    fish = serializers.CharField(read_only=True, source="fish.catch.grp")

    class Meta:
        model = FN127
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "species",
            "grp",
            "fish",
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
            "slug"
        )
