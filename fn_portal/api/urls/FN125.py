from django.urls import path

from ..views import (
    BioSampleList,
    FN125ListView,
    FN125DetailView,
    FN125LampreyReadOnlyList,
    FN125TagReadOnlyList,
)

urlpatterns = [
    path("fn125/", BioSampleList.as_view(), name="biosample_list"),
    path(
        ("<slug:prj_cd>/<slug:sample>/<str:effort>/<str:species>/<str:group>/"),
        FN125ListView.as_view(),
        name="FN125_listview",
    ),
    path("fn125/<slug:slug>/", FN125DetailView.as_view(), name="FN125_detailview"),
    path("fn125tags/", FN125TagReadOnlyList.as_view(), name="fn125tags_list"),
    path("fn125lamprey/", FN125LampreyReadOnlyList.as_view(), name="fn125lamprey_list"),
]
