from django.urls import path

from ..views import FN028DetailView, FN028ListView


urlpatterns = [
    path("fn028/", FN028ListView.as_view(), name="mode_list"),
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
]
