from django.urls import path

from ..views import FN013DetailView, FN013ListView

urlpatterns = [
    path("fn013/", FN013ListView.as_view(), name="fn013_list"),
    path("<str:prj_cd>/fn013", FN013ListView.as_view(), name="fn013-list"),
    path(
        "<str:prj_cd>/fn013/<str:gr>",
        FN013DetailView.as_view(),
        name="fn013-detail",
    ),
]
