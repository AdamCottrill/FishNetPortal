"""Urls for api endpoints for fn_portal

+ projects
+ <prj_cd>/sams
+ <prj_cd>/catcnts
+ <prj_cd>/biosamples

+ <prj_cd>/<sams>/<effs>

+ <prj_cd>/<sams>/<effs>/<spc>/<grp>/

"""


from django.urls import path, re_path

# from rest_framework import routers

from .views import (
    SpeciesListView,
    ProjectLeadListView,
    GearListView,
    LakeExtentListView,
    FNProtocolListView,
    # readonly endpoints:
    # FN011ViewSet,
    project_wizard,
    FN011ListView,
    FN011DetailView,
    FN013ListView,
    FN013DetailView,
    FN014ListView,
    FN014DetailView,
    FN022ListView,
    FN022DetailView,
    FN026ListView,
    FN026DetailView,
    FN028ListView,
    FN028DetailView,
    NetSetList,
    EffortList,
    CatchCountList,
    LengthTallyList,
    BioSampleList,
    FN125TagReadOnlyList,
    FN125LampreyReadOnlyList,
    FN126ReadOnlyList,
    FN127ReadOnlyList,
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

PRJ_CD_REGEX = r"(?P<prj_cd>[A-Za-z0-9]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$"

app_name = "fn_portal_api"

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register("fn011", FN011ViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path("", include(router.urls)),
    # =========================
    # READONLY ListViews:
    path("species_list/", SpeciesListView.as_view(), name="species_list"),
    path("prj_ldr/", ProjectLeadListView.as_view(), name="project_lead_list"),
    path("gear/", GearListView.as_view(), name="gear_list"),
    path("lakes/", LakeExtentListView.as_view(), name="lake_extent_list"),
    path("protocols/", FNProtocolListView.as_view(), name="protocol_list"),
    path("project_wizard/", project_wizard, name="project_wizard"),
    path("fn011/", FN011ListView.as_view(), name="project_list"),
    path("fn011/<slug:slug>/", FN011DetailView.as_view(), name="project_detail"),
    path("fn022/", FN022ListView.as_view(), name="season_list"),
    path("fn026/", FN026ListView.as_view(), name="space_list"),
    path("fn028/", FN028ListView.as_view(), name="mode_list"),
    path("fn121/", NetSetList.as_view(), name="netset_list"),
    path("fn122/", EffortList.as_view(), name="effort_list"),
    path("fn123/", CatchCountList.as_view(), name="catchcount_list"),
    path("fn124/", LengthTallyList.as_view(), name="fn124_list"),
    path("fn125/", BioSampleList.as_view(), name="biosample_list"),
    path("fn125tags/", FN125TagReadOnlyList.as_view(), name="fn125tags_list"),
    path("fn125lamprey/", FN125LampreyReadOnlyList.as_view(), name="fn125lamprey_list"),
    path("fn126/", FN126ReadOnlyList.as_view(), name="fn126_list"),
    path("fn127/", FN127ReadOnlyList.as_view(), name="fn127_list"),
    # =========================
    # CRUD ENDPOINTS:
    # FN121
    re_path(PRJ_CD_REGEX, FN121ListView.as_view(), name="FN121_listview"),
    path("<str:prj_cd>/fn013", FN013ListView.as_view(), name="fn013-list"),
    path(
        "<str:prj_cd>/fn013/<str:gr>",
        FN013DetailView.as_view(),
        name="fn013-detail",
    ),
    path("<str:prj_cd>/fn014/<str:gr>", FN014ListView.as_view(), name="fn014-list"),
    path(
        "<str:prj_cd>/fn014/<str:gr>/<str:eff>",
        FN014DetailView.as_view(),
        name="fn014-detail",
    ),
    path("<str:prj_cd>/seasons", FN022ListView.as_view(), name="fn022-list"),
    path(
        "<str:prj_cd>/season/<str:ssn>",
        FN022DetailView.as_view(),
        name="fn022-detail",
    ),
    path("<str:prj_cd>/spatial_strata", FN026ListView.as_view(), name="fn026-list"),
    path(
        "<str:prj_cd>/space/<str:space>",
        FN026DetailView.as_view(),
        name="fn026-detail",
    ),
    path(
        "<str:prj_cd>/modes",
        FN028ListView.as_view(),
        name="fn028-list",
    ),
    path(
        "<str:prj_cd>/mode/<str:mode>",
        FN028DetailView.as_view(),
        name="fn028-detail",
    ),
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
