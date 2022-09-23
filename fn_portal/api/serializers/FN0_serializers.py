"""Serializers for models in fn_portal"""
import re
from common.models import Lake
from django.contrib.auth import get_user_model
from fn_portal.models import (
    FNProtocol,
    FN011,
    FN012Base,
    FN012,
    FN012Protocol,
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

    def validate_prj_cd(self, value):
        """ensure that the project code is a valid FN-II project code"""

        pattern = "^[A-Z]{3}_[A-Z]{2}[0-9]{2}_[A-Z0-9]{3}$"

        if re.fullmatch(pattern, value) is None:
            raise serializers.ValidationError("That is not a valid FN-II project code.")
        return value

    def validate(self, data):
        """Make sure that:

        + start date occurs on or before end date,
        + start date and end date are in the same calendar year, and
        + that year in both dates agree with the year in prj_cd
        + project code siffux matches lake

        """

        if data["prj_date0"] > data["prj_date1"]:
            raise serializers.ValidationError(
                {"prj_date1": "project end date must occur on or after start date"}
            )

        if data["prj_date0"].year != data["prj_date1"].year:
            raise serializers.ValidationError(
                {"prj_date1": "project start and end occur in different years."}
            )

        prj_cd = data["prj_cd"]
        if str(data["prj_date0"].year)[2:] != prj_cd[6:8]:
            raise serializers.ValidationError(
                {
                    "prj_date0": "year of project start is not consistent with year in project code."
                }
            )

        if str(data["prj_date1"].year)[2:] != prj_cd[6:8]:
            raise serializers.ValidationError(
                {
                    "prj_date1": "year of project end is not consistent with year in project code."
                }
            )

        lake_project_prefixes = {
            "HU": ["LHA", "LHR"],
            "SU": ["LSA", "LSR"],
            "ON": ["LOA", "LOM"],
            "ER": ["LEA", "LEM"],
            "SC": ["LEA", "LEM"],
        }

        lake = data["lake"]
        suffix = data["prj_cd"][:3]
        if suffix not in lake_project_prefixes.get(lake.abbrev):
            raise serializers.ValidationError(
                {
                    "prj_cd": f"project code suffix ({suffix}) is not consistent with selected lake ({lake.abbrev})."
                }
            )

        data["status"] = "initiated"

        return data


class FN012BaseListSerializer(serializers.ModelSerializer):
    """A base class for our FN012 serailizers - inherted by FN012 and
    FN012Protocol serializers which add their key fields.  This
    serializer is not used directly.

    """

    spc = serializers.CharField(read_only=True, source="species.spc")

    class Meta:
        model = FN012Base
        fields = (
            "spc",
            "grp",
            "grp_des",
            "biosam",
            "sizsam",
            "sizatt",
            "sizint",
            "fdsam",
            "spcmrk",
            "agedec",
            "lamsam",
            "flen_min",
            "flen_max",
            "tlen_min",
            "tlen_max",
            "rwt_min",
            "rwt_max",
            "k_min_error",
            "k_min_warn",
            "k_max_error",
            "k_max_warn",
            "slug",
            "id",
        )


class FN012ListSerializer(FN012BaseListSerializer):
    """A readonly seralizer class that returns the sampling specs as
    expected from FN-II.  it is inherits from FN012Base and adds a
    field for project code.

    """

    prj_cd = serializers.CharField(read_only=True, source="project.prj_cd")

    class Meta:
        model = FN012
        fields = ("prj_cd",) + FN012BaseListSerializer.Meta.fields


class FN012ProtocolListSerializer(FN012BaseListSerializer):
    """A readonly seralizer class that returns the sampling specs as
    expected from FN-II for a specific protocol and lake.  it is
    inherits from FN012Base and adds a fields for protocol and lake.

    """

    protocol = serializers.CharField(read_only=True, source="protocol.abbrev")
    lake = serializers.CharField(read_only=True, source="lake.abbrev")

    class Meta:
        model = FN012Protocol
        fields = ("protocol", "lake") + FN012BaseListSerializer.Meta.fields


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


class FN013ListSerializer(serializers.ModelSerializer):
    """A class to list gears. This is a readonly seralizer that return the
    data as expected from FN-II. This serializer returns Gear objects
    in a format that emulates the FN013 records.  It does not include
    id or slug values as FN013 records do not actually exist.

    """

    prj_cd = serializers.CharField(read_only=True)
    gr = serializers.CharField(read_only=True, source="gr_code")

    class Meta:
        model = Gear
        fields = ("prj_cd", "gr", "effcnt", "effdst", "gr_des")


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


class FN022ListSerializer(serializers.ModelSerializer):
    """A class to list serializers. This is a readonly seralizer that return the data
    as expected from FN-II. Project is replaced by prj_cd.
    """

    prj_cd = serializers.CharField(read_only=True, source="project.prj_cd")

    class Meta:
        model = FN022
        fields = ("prj_cd", "ssn", "ssn_des", "ssn_date0", "ssn_date1", "slug", "id")


class FN022Serializer(serializers.ModelSerializer):
    """Class to serialize the seasons (temporal strata) used in each project."""

    project = serializers.SlugRelatedField(
        many=False, queryset=FN011.objects.all(), slug_field="slug"
    )

    class Meta:
        model = FN022
        fields = ("project", "ssn", "ssn_des", "ssn_date0", "ssn_date1", "slug")

    def validate(self, data):
        """Make sure that:

        + season start date occurs on or before end date,
        + season start date and end date are in the same calendar year, and
        + that year in both dates agree with the year in prj_cd

        """

        if data["ssn_date0"] > data["ssn_date1"]:
            raise serializers.ValidationError(
                {"ssn_date1": "season end date must occur on or after start date"}
            )

        if data["ssn_date0"].year != data["ssn_date1"].year:
            raise serializers.ValidationError(
                {"ssn_date1": "season start and end occur in different years."}
            )

        yr = data["project"].prj_cd[6:8]
        project_year = f"19{yr}" if int(yr) > 50 else f"20{yr}"

        if str(data["ssn_date0"].year) != project_year:
            raise serializers.ValidationError(
                {"ssn_date0": "season start year is not constistent with project year."}
            )

        if str(data["ssn_date1"].year) != project_year:
            raise serializers.ValidationError(
                {"ssn_date1": "season end year is not constistent with project year."}
            )

        return data


class FN026ListSerializer(serializers.ModelSerializer):
    """This is a super minimal serializer for spatial strata associated
    with a project. It is used by api endpoint to return read-only
    data in FN-II format. Fast and flat. The same as
    FN026SimpleSerializer but project is repalced with prj_cd.

    """

    prj_cd = serializers.CharField(read_only=True, source="project.prj_cd")

    class Meta:
        model = FN026
        fields = ("prj_cd", "space", "space_des", "dd_lat", "dd_lon", "slug", "id")


class FN026SimpleSerializer(serializers.ModelSerializer):
    """This is a super minimal serializer for creating spatial strata associated with
    a project. It is used by the project wizard convert the project
    code and and spatial strata information to database entries.

    This serializer is identical to the FN026ListSerializer except
    that the read-only field prj_cd has been replaced with a slug related field
    'project'

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


class FN026SubspaceSerializer(serializers.Serializer):
    """This is a super minimal serializer for spatial strata associated
    with a project. It is used by api endpoint to return read-only
    data in FN-II format. Fast and flat. The same as
    FN026SimpleSerializer but project is repalced with prj_cd.

    """

    prj_cd = serializers.CharField(read_only=True)
    space = serializers.CharField(read_only=True, source="space_code")
    subspace = serializers.CharField(read_only=True)
    subspace_des = serializers.CharField(read_only=True)
    dd_lat = serializers.FloatField(read_only=True)
    dd_lon = serializers.FloatField(read_only=True)
    slug = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)


class FN028ListSerializer(serializers.ModelSerializer):
    """This is a super minimal serializer for fishing mode associated with
    a project. It is used by api endpoint to return read-only data in
    FN-II format. Fast and flat. The same as FN028SimpleSerializer but
    project is repalced with prj_cd.

    """

    prj_cd = serializers.CharField(read_only=True, source="project.prj_cd")
    gear = serializers.CharField(read_only=True, source="gear.gr_code")

    class Meta:
        model = FN028
        fields = ("prj_cd", "mode", "mode_des", "gear", "gruse", "orient", "slug", "id")


class FN028SimpleSerializer(serializers.ModelSerializer):
    """This is a super minimal serializer for fishing mode associated with
    a project. It is used by the project wizard convert the project
    code and mode information to database entries.

    This serializer is identical to the FN028List Serializer except
    that the read-only field prj_cd has been replaced with a slug related field
    'project'

    """

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
