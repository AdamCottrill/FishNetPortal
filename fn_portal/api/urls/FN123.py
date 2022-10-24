from django.urls import path

from ..views import CatchCountList, FN123DetailView, FN123ListView, FN123NonFishList

urlpatterns = [
    path("fn123/", CatchCountList.as_view(), name="catchcount_list"),
    path(
        ("<slug:prj_cd>/<slug:sample>/<str:effort>"),
        FN123ListView.as_view(),
        name="FN123_listview",
    ),
    path("fn123/<slug:slug>/", FN123DetailView.as_view(), name="FN123_detailview"),
    path("fn123nonfish/", FN123NonFishList.as_view(), name="FN123NonFish_list"),
]
