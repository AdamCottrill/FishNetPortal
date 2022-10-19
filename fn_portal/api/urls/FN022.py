"""Urls for api endpoints for fn_portal

+ projects
+ <prj_cd>/sams
+ <prj_cd>/catcnts
+ <prj_cd>/biosamples

+ <prj_cd>/<sams>/<effs>

+ <prj_cd>/<sams>/<effs>/<spc>/<grp>/

"""


from django.urls import path, re_path

from ..views import (  # readonly endpoints:; FN011ViewSet,; CRUD Endpoints:
    FN022DetailView,
    FN022ListView,
)

urlpatterns = [
    path("fn022/", FN022ListView.as_view(), name="season_list"),
    path("<str:prj_cd>/seasons", FN022ListView.as_view(), name="fn022-list"),
    path(
        "<str:prj_cd>/season/<str:ssn>",
        FN022DetailView.as_view(),
        name="fn022-detail",
    ),
]
