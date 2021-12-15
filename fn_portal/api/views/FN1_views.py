"""Views for api endpoints."""

from django.contrib.postgres.aggregates import StringAgg
from django.db import transaction
from django.db.models import CharField, FilteredRelation, Q, F, Prefetch
from django.db.models.functions import Concat

from django.http import Http404
from common.models import ManagementUnit
from fn_portal.models import (
    FN011,
    FN121,
    FN122,
    FN123,
    FN124,
    FN125,
    FN126,
    FN127,
    FN125_Lamprey,
    FN125Tag,
)
from rest_framework import generics, status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response


from ...filters import (
    FN121Filter,
    FN122Filter,
    FN123Filter,
    FN124Filter,
    FN125Filter,
    FN125LampreyFilter,
    FN125TagFilter,
    FN126Filter,
    FN127Filter,
)
from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import (
    FN011WizardSerializer,
    FN022Serializer,
    FN022ListSerializer,
    FN026SimpleSerializer,
    FN028Serializer,
    FN028SimpleSerializer,
    FN121Serializer,
    FN121ReadOnlySerializer,
    FN121PostSerializer,
    FN122Serializer,
    FN123Serializer,
    FN124Serializer,
    FN125LampreySerializer,
    FN125Serializer,
    FN125ReadOnlySerializer,
    FN125TagSerializer,
    FN126Serializer,
    FN127Serializer,
    ProjectGearProcessTypeSerializer,
)
from ..utils import (
    StandardResultsSetPagination,
    LargeResultsSetPagination,
    XLargeResultsSetPagination,
    flatten_gear,
    check_distinct_seasons,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def project_wizard(request):
    """

    This api_view endpoint only accepts post requests generated from
    the FN project wizard. the response is a structured json object
    that contain elements for FN011, FN022, FN026, FN028, gear, and
    associated process types.  The entire function is wrapped in a
    transaction and only commits the data to the data base is the
    entire objects can be successfully parsed and converted into
    django objects.

    If the data is valid and all of the entities can be created, it
    returns a 200 response.  If there is an error anywhere in the
    parsing/validation process, a bad request response is retruned
    along with the associated errros object.

    """

    def serializeAndSave(items, serializer, project):
        """A helper function to serialize, validate and save each of our child
        elements. If there is a issued validateding any of the elements, the
        trasaction is rollback and an error response is returned.

        Arguments:
        - `items`:
        - `serializer`:
        - `project`:

        """

        for item in items:
            item["project"] = project.slug
            serialized_item = serializer(data=item)
            if serialized_item.is_valid(raise_exception=True):
                serialized_item.save()

    def duplicateCheck(label, data, fields):
        "raise an error if any of the values in fields are duplicated."
        for field in fields:
            values = [x.get(field) for x in data]
            if len(values) != len(list(set(values))):
                msg = {label: f"Duplicate values found for {field}."}
                raise serializers.ValidationError(msg)

    def duplicateModeAttributes(data):
        "raise an error if any of the values in fields are duplicated."
        values = [f"{x['gear']}-{x['set_type']}-{x['orient']}" for x in data]
        if len(values) != len(list(set(values))):
            msg = {
                "fn028": "Combinations of gear, orient, and set_type must be unique."
            }
            raise serializers.ValidationError(msg)

    if request.method == "POST":

        data = request.data

        fn011 = FN011WizardSerializer(data=data["fn011"])
        fn022 = data.get("fn022", [])
        fn026 = data.get("fn026", [])
        fn028 = data.get("fn028", [])

        gears = flatten_gear(data.get("gear_array", []))

        try:
            with transaction.atomic():

                if fn011.is_valid(raise_exception=True):
                    project = fn011.save()

                if len(fn022):
                    duplicateCheck(
                        "fn022", fn022, ["ssn", "ssn_des", "ssn_date0", "ssn_date1"]
                    )
                    if check_distinct_seasons(fn022) is False:
                        msg = {"fn022": "Seasons must be distinct and cannot overlap."}
                        raise serializers.ValidationError(msg)

                    serializeAndSave(fn022, FN022Serializer, project)
                else:
                    msg = {"fn022": "At least one season must be specified"}
                    raise serializers.ValidationError(msg)

                if len(fn026):
                    duplicateCheck("fn026", fn026, ["space", "space_des"])
                    serializeAndSave(fn026, FN026SimpleSerializer, project)
                else:
                    msg = {"fn026": "At least one spatial strata must be specified"}
                    raise serializers.ValidationError(msg)

                if len(fn028):
                    duplicateCheck("fn028", fn028, ["mode", "mode_des"])
                    duplicateModeAttributes(fn028)
                    serializeAndSave(fn028, FN028SimpleSerializer, project)
                else:
                    msg = {"fn028": "At least one mode must be specified"}
                    raise serializers.ValidationError(msg)
                if len(gears):
                    serializeAndSave(gears, ProjectGearProcessTypeSerializer, project)
                else:
                    msg = {
                        "gear_array": "At least one gear and process type must be specified"
                    }
                    raise serializers.ValidationError(msg)

        except serializers.ValidationError as error:

            return Response(error.args, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"message": "Success!", "data": request.data},
            status=status.HTTP_201_CREATED,
        )


class NetSetList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN121ReadOnlySerializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN121Filter

    def get_queryset(self):

        mu_type = self.request.query_params.get("mu_type")

        if mu_type:
            mus = ManagementUnit.objects.filter(mu_type=mu_type).defer("geom")
        else:
            mus = ManagementUnit.objects.filter(primary=True).defer("geom")

        prefetched = Prefetch("management_units", queryset=mus, to_attr="mu")

        queryset = (
            (
                FN121.objects.select_related(
                    "project", "grid5", "grid5__lake", "ssn", "space", "mode"
                )
                .prefetch_related(prefetched)
                .defer(
                    "grid5__geom",
                    "grid5__envelope",
                    "grid5__centroid",
                    "grid5__lake__geom",
                    "grid5__lake__geom_ontario",
                    "grid5__lake__envelope",
                    "grid5__lake__envelope_ontario",
                    "grid5__lake__centroid",
                    "grid5__lake__centroid_ontario",
                )
            )
            .order_by("slug")
            .all()
            .distinct()
        )

        return queryset


class EffortList(generics.ListAPIView):
    """A read-only endpoint to return effort (gill net panels or trap net
    lifts) objects.  Accepts query parameter filters for year, project
    codes, site depth, lift and set dates and times, gear types, and
    grid(s).

    """

    serializer_class = FN122Serializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN122Filter
    queryset = (
        FN122.objects.select_related("sample", "sample__project")
        .order_by("slug")
        .annotate(prj_cd=F("sample__project__prj_cd"), sam=F("sample__sam"))
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "effdst",
            "grdep",
            "grtem0",
            "grtem1",
            "slug",
        )
    )


class CatchCountList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN123Serializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN123Filter

    queryset = (
        FN123.objects.select_related(
            "species", "effort", "effort__sample", "effort__sample__project"
        )
        .exclude(species__spc="000")
        .order_by("slug")
        .annotate(
            prj_cd=F("effort__sample__project__prj_cd"),
            sam=F("effort__sample__sam"),
            eff=F("effort__eff"),
            spc=F("species__spc"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "catcnt",
            "catwt",
            "biocnt",
            "comment3",
            "slug",
        )
    )


class LengthTallyList(generics.ListAPIView):
    """A read-only endpoint to return length tally objects.  Accepts query
    parameter filters for attributes of the length tally, the catch,
    the effort, the sample and the project.

    """

    serializer_class = FN124Serializer
    pagination_class = LargeResultsSetPagination
    filterset_class = FN124Filter

    queryset = (
        FN124.objects.select_related(
            "catch__species",
            "catch__effort",
            "catch__effort__sample",
            "catch__effort__sample__project",
        )
        .exclude(catch__species__spc="000")
        .annotate(
            prj_cd=F("catch__effort__sample__project__prj_cd"),
            sam=F("catch__effort__sample__sam"),
            eff=F("catch__effort__eff"),
            spc=F("catch__species__spc"),
            grp=F("catch__grp"),
        )
        .order_by("slug")
    )


class BioSampleList(generics.ListAPIView):
    """A read-only endpoint to return net set objects.  Accepts query
    parameter filters for year, project codes, site depth, lift and
    set dates and times, gear types, and grid(s).

    """

    serializer_class = FN125ReadOnlySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN125Filter
    queryset = (
        FN125.objects.select_related(
            "catch",
            "catch__species",
            "catch__effort__sample",
            "catch__effort__sample__project",
        )
        .order_by("slug")
        .prefetch_related("age_estimates")
        .annotate(
            preferred_age=FilteredRelation(
                "age_estimates", condition=Q(age_estimates__preferred=True)
            )
        )
        .annotate(
            prj_cd=F("catch__effort__sample__project__prj_cd"),
            sam=F("catch__effort__sample__sam"),
            eff=F("catch__effort__eff"),
            spc=F("catch__species__spc"),
            grp=F("catch__grp"),
            age=F("preferred_age__agea"),
            # lamijc=StringAgg(
            #     Concat(
            #         "lamprey_marks__lamijc_type",
            #         "lamprey_marks__lamijc_size",
            #         output_field=CharField(),
            #     ),
            #     "",
            # ),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
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
            "age",
            # "lamijc",
            "comment5",
            "slug",
        )
    )


class FN125LampreyReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects.

    TODO - add filter for FN125Lamprey objects

    """

    serializer_class = FN125LampreySerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN125LampreyFilter
    queryset = (
        FN125_Lamprey.objects.select_related(
            "fish",
            "fish__catch",
            "fish__catch__species",
            "fish__catch__effort__sample",
            "fish__catch__effort__sample__project",
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("fish__catch__effort__sample__project__prj_cd"),
            sam=F("fish__catch__effort__sample__sam"),
            eff=F("fish__catch__effort__eff"),
            spc=F("fish__catch__species__spc"),
            grp=F("fish__catch__grp"),
            fishn=F("fish__fish"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fishn",
            "lamid",
            "xlam",
            "lamijc_type",
            "lamijc_size",
            "comment_lam",
            "slug",
        )
    )


class FN125TagReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return fish tags that have been either
    applied or recoved."""

    serializer_class = FN125TagSerializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN125TagFilter
    queryset = (
        FN125Tag.objects.select_related(
            "fish",
            "fish__catch",
            "fish__catch__species",
            "fish__catch__effort__sample",
            "fish__catch__effort__sample__project",
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("fish__catch__effort__sample__project__prj_cd"),
            sam=F("fish__catch__effort__sample__sam"),
            eff=F("fish__catch__effort__eff"),
            spc=F("fish__catch__species__spc"),
            grp=F("fish__catch__grp"),
            fishn=F("fish__fish"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fishn",
            "fish_tag_id",
            "tagstat",
            "tagid",
            "tagdoc",
            "xcwtseq",
            "xtaginckd",
            "xtag_chk",
            "comment_tag",
            "slug",
        )
    )


class FN126ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return diet objects."""

    serializer_class = FN126Serializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN126Filter
    queryset = (
        FN126.objects.select_related(
            "fish",
            "fish__catch",
            "fish__catch__species",
            "fish__catch__effort__sample",
            "fish__catch__effort__sample__project",
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("fish__catch__effort__sample__project__prj_cd"),
            sam=F("fish__catch__effort__sample__sam"),
            eff=F("fish__catch__effort__eff"),
            spc=F("fish__catch__species__spc"),
            grp=F("fish__catch__grp"),
            fishn=F("fish__fish"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fishn",
            "food",
            "taxon",
            "foodcnt",
            "comment6",
            "slug",
        )
    )


class FN127ReadOnlyList(generics.ListAPIView):
    """A read-only endpoint to return age estimates objects.

    TODO - add filter for FN126 objects

    """

    serializer_class = FN127Serializer
    pagination_class = XLargeResultsSetPagination
    filterset_class = FN127Filter
    queryset = (
        FN127.objects.select_related(
            "fish",
            "fish__catch",
            "fish__catch__species",
            "fish__catch__effort__sample",
            "fish__catch__effort__sample__project",
        )
        .order_by("slug")
        .annotate(
            prj_cd=F("fish__catch__effort__sample__project__prj_cd"),
            sam=F("fish__catch__effort__sample__sam"),
            eff=F("fish__catch__effort__eff"),
            spc=F("fish__catch__species__spc"),
            grp=F("fish__catch__grp"),
            fishn=F("fish__fish"),
        )
        .values(
            "id",
            "prj_cd",
            "sam",
            "eff",
            "spc",
            "grp",
            "fishn",
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
    )


# ========================================================
#      RETRIEVE-UPDATE-DESTROY

# these views will be used to get, update and delete individual
# records for netsets, efforts, catch counts and bio-samples.


class FN121ListView(generics.ListCreateAPIView):
    """An api end point for listing net sets within a project. A new net
    set can be created by posting to this endpoint.  A get request
    will return a json response containing all of the net sets
    associated with the project identifed by the project code in the url.

    TODO:

    + add filters for gear type, depth, active (lifttime=null)

    """

    permission_classes = [IsAdminUser | IsPrjLeadCrewOrAdminOrReadOnly]
    filterset_class = FN121Filter
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """our get and post serializiers have different fields for ssn, space
        and mode - get has object labels, post expects slugs."""
        if self.request.method == "GET":
            return FN121Serializer
        return FN121PostSerializer

    def get_project(self):
        """

        Arguments:
        - `self`:
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        try:
            project = FN011.objects.defer(
                "lake__geom",
                "lake__geom_ontario",
                "lake__envelope",
                "lake__envelope_ontario",
                "lake__centroid",
                "lake__centroid_ontario",
            ).get(slug=prj_cd)

            return project

        except FN011.DoesNotExist:
            raise Http404

    def get_queryset(self):
        """
        This view should return a list of all the net sets for a project
        as determined by the slug portion of the URL.
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        queryset = (
            FN121.objects.filter(project__slug=prj_cd)
            .select_related("grid5", "grid5__lake")
            .defer(
                "grid5__geom",
                "grid5__envelope",
                "grid5__centroid",
                "grid5__lake__geom",
                "grid5__lake__geom_ontario",
                "grid5__lake__envelope",
                "grid5__lake__envelope_ontario",
                "grid5__lake__centroid",
                "grid5__lake__centroid_ontario",
            )
        )

        return queryset

    def get_serializer_context(self):
        """to create a new net set, we have to make the project available in
        the serializer's context"""

        context = super(FN121ListView, self).get_serializer_context()
        project = self.get_project()
        context.update({"project": project})
        return context


class FN121DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual net sets with GET, PATCH, and DELETE requests.
    Requires a unique slug value to identify the net set.  THe slug is
    of the form: <prj_cd>-<sam>.

    e.g. - lha_ia01_023-1

    """

    permission_classes = [IsAdminUser | IsPrjLeadCrewOrAdminOrReadOnly]
    # serializer_class = FN121PostSerializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN121.objects.all()

    def get_serializer_class(self):
        """our get and post serializiers have different fields for ssn, space
        and mode - get has object labels, post expects slugs."""
        if self.request.method == "GET":
            return FN121Serializer
        return FN121PostSerializer


class FN122ListView(generics.ListCreateAPIView):
    """A view to return all of the efforts associated with a net set
    (within a project).

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN122Serializer

    def get_queryset(self):
        """
        This view should return a list of all the efforts for the net set identified by the
        project code and sample number.
        """
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs["sample"]

        queryset = FN122.objects.select_related("sample", "sample__project").filter(
            sample__project__slug=prj_cd, sample__sam=sam
        )

        return queryset


class FN122DetailView(generics.RetrieveUpdateDestroyAPIView):

    """An classed based view that provides a way to retrieve, update and
    delete individual efforts within a net set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the effort
    set.  THe slug is of the form: <prj_cd>-<sam>-<eff>.

    e.g. - lha_ia01_023-1-051

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN122Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN122.objects.all()


class FN123ListView(generics.ListCreateAPIView):
    """A view to return all of the catch counts associated with a project

    TODO: filter by SAM, EFF, SPC (and maybe GRP?)
    """

    serializer_class = FN123Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        queryset = (
            FN123.objects.select_related(
                "species", "effort", "effort__sample", "effort__sample__project"
            )
            .filter(
                effort__sample__project__slug=prj_cd,
                effort__sample__sam=sam,
                effort__eff=eff,
            )
            .exclude(species__spc="000")
        )

        return queryset

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(FN123ListView, self).get_serializer_context()
        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")

        if sam and eff:
            effort = FN122.objects.select_related("sample", "sample__project").get(
                sample__project__slug=prj_cd, sample__sam=sam, eff=eff
            )
            context.update({"effort": effort})

        return context


class FN123DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual catch counts within an effort set with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the catch count
    (including both species and group code).  THe slug is of the form:
    <prj_cd>-<sam>-<eff>-<spc>-<grp>.

    e.g. - lha_ia01_023-1-051-331-00

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN123Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN123.objects.all()


class FN125ListView(generics.ListCreateAPIView):
    """A view to return all of the biosamples assocaited with an FN123
    record (by effort, species and grp) or to create a new FN125 record.

    if you are looking for all biosamples, see biosamples/ and
    <prj_cd>/biosamples endpoints.

    NOTES:

    + we could add filters to these at some point (find fish with
    specific attributes).

    + create has not yet been implemented.

    """

    serializer_class = FN125Serializer
    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]

    def get_serializer_context(self):
        """to create a new catch count, we have to make the effort available in
        the serializer's context"""

        context = super(FN125ListView, self).get_serializer_context()

        prj_cd = self.kwargs.get("prj_cd", "").lower()
        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        context.update(
            {
                "catch_count": FN123.objects.get(
                    effort__sample__project__slug=prj_cd,
                    effort__sample__sam=sam,
                    effort__eff=eff,
                    species__spc=spc,
                    grp=grp,
                )
            }
        )

        return context

    def get_queryset(self):
        """"""
        prj_cd = self.kwargs.get("prj_cd", "").lower()

        sam = self.kwargs.get("sample")
        eff = self.kwargs.get("effort")
        spc = self.kwargs.get("species")
        grp = self.kwargs.get("group")

        queryset = (
            FN125.objects.select_related(
                "catch",
                "catch__species",
                "catch__effort__sample",
                "catch__effort__sample__project",
            )
            .prefetch_related("fishtags", "lamprey_marks", "diet_data", "age_estimates")
            .filter(
                catch__effort__sample__project__slug=prj_cd,
                catch__effort__sample__sam=sam,
                catch__effort__eff=eff,
                catch__species__spc=spc,
                catch__grp=grp,
            )
        )

        return queryset


class FN125DetailView(generics.RetrieveUpdateDestroyAPIView):
    """An classed based view that provides a way to retrieve, update and
    delete individual fish within an catch count with GET, PATCH, and
    DELETE requests.  Requires a unique slug value to identify the
    fish.  THe slug is of the form: <prj_cd>-<sam>-<eff>-<spc>-<grp>-<fish>.

    e.g. - lha_ia01_023-1-051-331-00-1

    """

    permission_classes = [IsPrjLeadCrewOrAdminOrReadOnly]
    serializer_class = FN125Serializer
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = FN125.objects.all()
