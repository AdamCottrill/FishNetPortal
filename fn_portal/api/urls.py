"""Urls for api endpoints for fn_portal

+ projects
+ <prj_cd>/sams
+ <prj_cd>/catcnts
+ <prj_cd>/biosamples

+ <prj_cd>/<sams>/<effs>

+ <prj_cd>/<sams>/<effs>/<spc>/<grp>/

"""

from django.conf.urls import url
from django.urls import include, path

from rest_framework import routers

from .views import (
    SpeciesList,
    FN011ViewSet,
    NetSetList,
    CatchCountList,
    BioSampleList,
    EffortList,
    FN121DetailView,
    FN122DetailView,
    FN123DetailView,
    FN125DetailView,
)

app_name = "fn_portal_api"


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register("project", FN011ViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r"^", include(router.urls)),
    url("^species_list$", SpeciesList.as_view(), name="species-list"),
    url("^net_sets/(?P<slug>.+)/$", NetSetList.as_view(), name="project-samples"),
    url(
        "^catch_counts/(?P<slug>.+)/$",
        CatchCountList.as_view(),
        name="project-catch-counts",
    ),
    url(
        "^biosamples/(?P<slug>.+)/$",
        BioSampleList.as_view(),
        name="project-bio-samples",
    ),
    url(
        "(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/samples$",
        NetSetList.as_view(),
        name="project-samples2",
    ),
    url(
        "(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/(?P<sample>.+)/efforts$",
        EffortList.as_view(),
        name="sample-efforts",
    ),
    url(
        (
            "(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/(?P<sample>.+)"
            + "/(?P<effort>.+)/catch_counts$"
        ),
        CatchCountList.as_view(),
        name="efforts-catches",
    ),
    url(
        (
            "(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/(?P<sample>.+)"
            + "/(?P<effort>.+)/(?P<species>.+)/(?P<group>.+)/biosamples$"
        ),
        BioSampleList.as_view(),
        name="catch-biosamples",
    ),
    path("fn121/<str:slug>/", FN121DetailView.as_view(), name="FN121_detail_view"),
    path("fn122/<str:slug>/", FN122DetailView.as_view(), name="FN122_detail_view"),
    path("fn123/<str:slug>/", FN123DetailView.as_view(), name="FN123_detail_view"),
    path("fn125/<str:slug>/", FN125DetailView.as_view(), name="FN125_detail_view"),
]


# <prj_cd>
# <prj_cd>/samples

# <prj_cd>/<sam>/
# <prj_cd>/<sam>/efforts

# <prj_cd>/<sam>/<eff>
# <prj_cd>/<sam>/<eff>/catcnts

# <prj_cd>/<sam>/<eff>/<spc>/<grp>
# <prj_cd>/<sam>/<eff>/<spc>/<grp>/biosamples


# <prj_cd>/<sam>/<eff>/<spc>/<grp>/<fish>
# These should be added as nested objects:
# <prj_cd>/<sam>/<eff>/<spc>/<grp>/<fish>tags
# <prj_cd>/<sam>/<eff>/<spc>/<grp>/<fish>lamprey
# <prj_cd>/<sam>/<eff>/<spc>/<grp>/<fish>age_estimates
