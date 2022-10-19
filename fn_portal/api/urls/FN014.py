from django.urls import path

from ..views import FN014DetailView, FN014ListView

urlpatterns = [
    path("<str:prj_cd>/fn014/<str:gr>", FN014ListView.as_view(), name="fn014-list"),
    path(
        "<str:prj_cd>/fn014/<str:gr>/<str:eff>",
        FN014DetailView.as_view(),
        name="fn014-detail",
    ),
]
