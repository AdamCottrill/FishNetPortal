from django.conf import settings
from django.urls import path, re_path


from ..views import (  # readonly endpoints:; FN011ViewSet,; CRUD Endpoints:
    FN121DetailView,
    FN121ListView,
    FN121LimnoList,
    NetSetList,
)


PRJ_CD_REGEX = settings.PRJ_CD_URL_REGEX

urlpatterns = [
    path("fn121/", NetSetList.as_view(), name="netset_list"),
    re_path(f"{PRJ_CD_REGEX}/$", FN121ListView.as_view(), name="FN121_listview"),
    path("fn121/<slug:slug>/", FN121DetailView.as_view(), name="FN121_detailview"),
    path("fn121limno/", FN121LimnoList.as_view(), name="fn121limno_list"),
]
