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
    EffortList,
    FN122DetailView,
    FN122ListView,
    FN121GpsTrackList,
)

urlpatterns = [
    path("fn122/", EffortList.as_view(), name="effort_list"),
    path("<slug:prj_cd>/<str:sample>", FN122ListView.as_view(), name="FN122_listview"),
    path("fn122/<slug:slug>/", FN122DetailView.as_view(), name="FN122_detailview"),
    path("fn121GpsTracks/", FN121GpsTrackList.as_view(), name="fn121_gpstrack_list"),
]
