"""Urls for api endpoints for fn_portal

+ projects
+ <prj_cd>/sams
+ <prj_cd>/catcnts
+ <prj_cd>/biosamples

+ <prj_cd>/<sams>/<effs>

+ <prj_cd>/<sams>/<effs>/<spc>/<grp>/

"""


from django.urls import include, path

from rest_framework import routers

from .views import (
    SpeciesList,
    # readonly endpoints:
    FN011ViewSet,
    NetSetList,
    EffortList,
    CatchCountList,
    BioSampleList,
    # CRUD Endpoints:
    FN121ListView,
    FN121DetailView,
    FN122ListView,
    FN122DetailView,
    FN123ListView,
    FN123DetailView,
    FN125ListView,
    FN125DetailView,
)

app_name = "fn_portal_api"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register("project", FN011ViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("species_list/", SpeciesList.as_view(), name="species-list"),
    # these three urls are configured  with slug at the end. Is this what we want?
    path(
        "catch_counts/<slug:slug>/",
        CatchCountList.as_view(),
        name="project-catch-counts",
    ),
    # =========================
    # READONLY ListViews:
    path("fn121/", NetSetList.as_view(), name="netset-list"),
    path("fn125/", BioSampleList.as_view(), name="biosample-list"),
    # =========================
    # CRUD ENDPOINTS:
    # these urls are configured <prj_cd>/<sam>/<eff>
    # path("<slug:slug>/samples/", NetSetList.as_view(), name="project-samples2"),
    # FN121
    path("<slug:prj_cd>/", FN121ListView.as_view(), name="FN121_listview"),
    path("fn121/<slug:slug>/", FN121DetailView.as_view(), name="FN121_detailview"),
    # FN122
    path("<slug:prj_cd>/<str:sample>", FN122ListView.as_view(), name="FN122_listview"),
    path("fn122/<slug:slug>/", FN122DetailView.as_view(), name="FN122_detailview"),
    # FN123
    path(
        ("<slug:prj_cd>/<slug:sample>/<str:effort>"),
        FN123ListView.as_view(),
        name="FN123_listview",
    ),
    path("fn123/<slug:slug>/", FN123DetailView.as_view(), name="FN123_detailview"),
    # FN125
    path(
        ("<slug:prj_cd>/<slug:sample>/<str:effort>/<str:species>/<str:group>/"),
        FN125ListView.as_view(),
        name="FN125_listview",
    ),
    path("fn125/<slug:slug>/", FN125DetailView.as_view(), name="FN125_detailview"),
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
