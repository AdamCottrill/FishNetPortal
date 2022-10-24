"""Serializers for models in fn_portal"""

from common.models import Grid5
from fn_portal.models import (
    FN011,
    FN022,
    FN026Subspace,
    FN028,
    FN121,
    FN121Limno,
    FN122,
    FN123,
    FN124,
    FN125,
    FN126,
    FN127,
    FN125_Lamprey,
    FN125Tag,
)
from rest_framework import serializers

from .common_serializers import GridSerializer
from .FN0_serializers import FN022Serializer, FN026Serializer, FN028Serializer


class FN121Serializer(serializers.ModelSerializer):
    """a serializer for returning FN121 objects"""

    prj_cd = serializers.CharField(source="project.prj_cd")
    ssn = serializers.CharField(source="ssn.ssn")
    space = serializers.CharField(source="subspace.space.space")
    subspace = serializers.CharField(source="subspace.subspace")
    mode = serializers.CharField(source="mode.mode")
    grid5 = serializers.CharField(source="grid5.grid")

    effdt0 = serializers.DateField(format="%Y-%m-%d")
    effdt1 = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = FN121
        lookup_field = "slug"
        # need to get prj_cd from FN011 table.

        fields = (
            "id",
            "prj_cd",
            "sam",
            "ssn",
            "space",
            "subspace",
            "mode",
            "effdt0",
            "effdt1",
            "effdur",
            "efftm0",
            "efftm1",
            "effst",
            "sidep0",
            "sidep1",
            "grdepmax",
            "grdepmin",
            "site",
            "sitp",
            "grid5",
            "dd_lat0",
            "dd_lon0",
            "dd_lat1",
            "dd_lon1",
            "sitem0",
            "sitem1",
            "secchi0",
            # "secchi1",
            "slime",
            "crew",
            # "process_type",
            "comment1",
            "slug",
        )

        read_only_fields = ("slug", "id")


class FN121ReadOnlySerializer(FN121Serializer):
    """a serializer for returning FN121 objects"""

    management_unit = serializers.SerializerMethodField()

    class Meta:
        model = FN121

        fields = FN121Serializer.Meta.fields + ("management_unit",)

    def get_management_unit(self, obj):

        if obj.mu:
            return obj.mu[0].slug
        else:
            return None


class FN121PostSerializer(FN121Serializer):

    project = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field="prj_cd", queryset=FN011.objects.all()
    )

    ssn = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field="slug", queryset=FN022.objects.all()
    )

    subspace = serializers.SlugRelatedField(
        many=False,
        read_only=False,
        slug_field="slug",
        queryset=FN026Subspace.objects.all(),
    )

    mode = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field="slug", queryset=FN028.objects.all()
    )
    grid5 = serializers.SlugRelatedField(
        many=False, read_only=False, slug_field="slug", queryset=Grid5.objects.all()
    )

    class Meta:
        model = FN121
        lookup_field = "slug"

        fields = (
            "id",
            "project",
            "sam",
            "ssn",
            "subspace",
            "mode",
            "effdt0",
            "effdt1",
            "effdur",
            "efftm0",
            "efftm1",
            "effst",
            "sidep0",
            "sidep1",
            "site",
            "grid5",
            "dd_lat0",
            "dd_lon0",
            "dd_lat1",
            "dd_lon1",
            "sitem0",
            "sitem1",
            "comment1",
            "secchi0",
            # "secchi1",
            "slug",
        )

        read_only_fields = ("slug", "id")


class FN121LimnoSerializer(serializers.ModelSerializer):
    """A serializer for limnological (water chemistry) data associated with
    a particular net set."""

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)

    class Meta:
        model = FN121Limno

        fields = (
            "prj_cd",
            "sam",
            "o2gear0",
            "o2gear1",
            "o2bot0",
            "o2bot1",
            "o2surf0",
            "o2surf1",
            "slug",
        )


class FN121TrapnetReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN121Trapnet data. Used by
    get_fn121_trapnet endpoint."""

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    cover_type = serializers.CharField(read_only=True)
    bottom_type = serializers.CharField(read_only=True)
    vegetation = serializers.IntegerField(read_only=True)
    lead_angle = serializers.FloatField(read_only=True)
    leaduse = serializers.FloatField(read_only=True)
    distoff = serializers.FloatField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN121TrawlReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN121Trawl data. Used by
    get_fn121_trawl endpoint."""

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    vessel = serializers.CharField(read_only=True, source="vessel_abbrev")
    vessel_speed = serializers.FloatField(read_only=True)
    vessel_direction = serializers.IntegerField(read_only=True)
    warp = serializers.FloatField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN121WeatherReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN121Trawl data. Used by
    get_fn121_trawl endpoint."""

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)

    airtem0 = serializers.FloatField(read_only=True)
    airtem1 = serializers.FloatField(read_only=True)
    wind0 = serializers.CharField(read_only=True)
    wind1 = serializers.CharField(read_only=True)
    precip0 = serializers.CharField(read_only=True)
    precip1 = serializers.CharField(read_only=True)
    cloud_pc0 = serializers.FloatField(read_only=True)
    cloud_pc1 = serializers.FloatField(read_only=True)
    waveht0 = serializers.FloatField(read_only=True)
    waveht1 = serializers.FloatField(read_only=True)
    xweather = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN122ReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN122 objects. Used by get_fn122 endpoint."""

    id = serializers.IntegerField(read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    effdst = serializers.FloatField(read_only=True)
    grdep0 = serializers.FloatField(read_only=True)
    grdep1 = serializers.FloatField(read_only=True)
    grtem0 = serializers.FloatField(read_only=True)
    grtem1 = serializers.FloatField(read_only=True)
    efftm0 = serializers.TimeField(read_only=True)
    efftm1 = serializers.TimeField(read_only=True)
    waterhaul = serializers.BooleanField(read_only=True)
    comment2 = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN122Serializer(serializers.ModelSerializer):
    """"""

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)

    class Meta:
        model = FN122

        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "effdst",
            "grdep0",
            "grdep1",
            "grtem0",
            "grtem1",
            "efftm0",
            "efftm1",
            "waterhaul",
            "comment2",
            "slug",
        )

    def create(self, validated_data):
        """When we create an effort object, we need to add the associated
        sample (net set)."""

        validated_data["sample"] = self.context["sample"]
        return FN122.objects.create(**validated_data)


class FN122TransectReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN122Transect objects. Used by get_fn122transect endpoint."""

    id = serializers.IntegerField(read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    track_id = serializers.IntegerField(read_only=True)
    sidep = serializers.FloatField(read_only=True)
    timestamp = serializers.DateTimeField(read_only=True)
    geom = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)
    comment2 = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN123Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)

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
            "subcnt",
            "subwt",
            "comment3",
            "slug",
        )

    def create(self, validated_data):
        """When we create new catch count object, we need to add the associated
        effort (within a net within a project)."""

        validated_data["effort"] = self.context["effort"]
        return FN123.objects.create(**validated_data)


class FN123NonFishReadOnlySerializer(serializers.Serializer):
    """A read-only serializer for FN123 Non-fish objects. Used by
    get_fn123NonFish endpoint."""

    id = serializers.IntegerField(read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    taxon = serializers.CharField(read_only=True, source="taxon_code")
    catcnt = serializers.IntegerField(read_only=True)
    mortcnt = serializers.IntegerField(read_only=True)
    comment3 = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN124Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)

    class Meta:
        model = FN124
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "siz",
            "sizcnt",
            "slug",
        )

    def create(self, validated_data):
        """When we create new catch count object, we need to add the associated
        catch"""

        validated_data["catch"] = self.context["catch"]
        return FN124.objects.create(**validated_data)


class FN125TagNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN125Tag
        fields = (
            "id",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "cwtseq",
            "tag_checked",
            "comment_tag",
        )


class FN125LampreyNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN125_Lamprey
        fields = (
            "id",
            "lamid",
            "xlam",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
        )


class FN126NestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FN126
        fields = ("id", "food", "taxon", "fdcnt", "comment6")


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


class FN125ReadOnlySerializer(serializers.Serializer):
    """ """

    id = serializers.IntegerField(read_only=True)
    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True)
    flen = serializers.FloatField(read_only=True)
    tlen = serializers.FloatField(read_only=True)
    rwt = serializers.FloatField(read_only=True)
    eviswt = serializers.FloatField(read_only=True)
    girth = serializers.FloatField(read_only=True)
    clipc = serializers.CharField(read_only=True)
    clipa = serializers.CharField(read_only=True)
    sex = serializers.CharField(read_only=True)
    mat = serializers.CharField(read_only=True)
    gon = serializers.CharField(read_only=True)
    noda = serializers.CharField(read_only=True)
    nodc = serializers.CharField(read_only=True)
    agest = serializers.CharField(read_only=True)
    fate = serializers.CharField(read_only=True)
    age = serializers.IntegerField(read_only=True)
    tissue = serializers.CharField(read_only=True)
    age_flag = serializers.CharField(read_only=True)
    lam_flag = serializers.CharField(read_only=True)
    stom_flag = serializers.CharField(read_only=True)
    tag_flag = serializers.CharField(read_only=True)
    comment5 = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)


class FN125Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(
        read_only=True, source="catch.effort.sample.project.prj_cd"
    )
    sam = serializers.CharField(read_only=True, source="catch.effort.sample.sam")
    species = serializers.CharField(read_only=True, source="catch.species.spc")
    eff = serializers.CharField(read_only=True, source="catch.effort.eff")
    grp = serializers.CharField(read_only=True, source="catch.grp")

    # child tables
    lamprey_marks = FN125LampreyNestedSerializer(
        many=True, required=False, allow_null=True
    )
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
            "eviswt",
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

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="fishn")

    class Meta:
        model = FN125Tag
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fish",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "cwtseq",
            "tag_checked",
            "comment_tag",
            "slug",
        )


class FN125LampreySerializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="fishn")

    class Meta:
        model = FN125_Lamprey
        fields = (
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fish",
            "id",
            "lamid",
            "xlam",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
            "slug",
        )


class FN126Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="fishn")

    class Meta:
        model = FN126
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fish",
            "food",
            "taxon",
            "fdcnt",
            "comment6",
            "slug",
        )


class FN127Serializer(serializers.ModelSerializer):

    prj_cd = serializers.CharField(read_only=True)
    sam = serializers.CharField(read_only=True)
    eff = serializers.CharField(read_only=True)
    spc = serializers.CharField(read_only=True)
    grp = serializers.CharField(read_only=True)
    fish = serializers.CharField(read_only=True, source="fishn")

    class Meta:
        model = FN127
        fields = (
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
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
            "slug",
        )
