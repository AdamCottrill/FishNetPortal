from rest_framework import generics


from django.db.models import FilteredRelation, Q, F

from fn_portal.models import FN123, FN125

from ...filters import FN125Filter

from ..permissions import IsPrjLeadCrewOrAdminOrReadOnly
from ..serializers import (
    FN125Serializer,
    FN125ReadOnlySerializer,
)
from ..utils import XLargeResultsSetPagination


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
            "eviswt",
            "girth",
            "clipa",
            "clipc",
            "sex",
            "mat",
            "gon",
            "gonwt",
            "noda",
            "nodc",
            "agest",
            "tissue",
            "stom_flag",
            "fate",
            "age",
            # "lamijc",
            "comment5",
            "slug",
        )
    )


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
