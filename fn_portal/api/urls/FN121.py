from django.conf import settings
from django.urls import path, re_path


from ..views import (  # readonly endpoints:; FN011ViewSet,; CRUD Endpoints:
    FN121DetailView,
    FN121ListView,
    FN121LimnoList,
    FN121TrapnetList,
    FN121TrawlList,
    FN121WeatherList,
    FN121ElectroFishingList,
    NetSetList,
)


PRJ_CD_REGEX = settings.PRJ_CD_URL_REGEX

urlpatterns = [
    path("fn121/", NetSetList.as_view(), name="netset_list"),
    re_path(f"{PRJ_CD_REGEX}/$", FN121ListView.as_view(), name="FN121_listview"),
    path("fn121/<slug:slug>/", FN121DetailView.as_view(), name="FN121_detailview"),
    path("fn121limno/", FN121LimnoList.as_view(), name="fn121limno_list"),
    path("fn121trapnet/", FN121TrapnetList.as_view(), name="fn121trapnet_list"),
    path("fn121trawl/", FN121TrawlList.as_view(), name="fn121trawl_list"),
    path("fn121weather/", FN121WeatherList.as_view(), name="fn121weather_list"),
    path(
        "fn121electrofishing/",
        FN121ElectroFishingList.as_view(),
        name="fn121electrofishing_list",
    ),
]
