from django.conf import settings
from django.urls import path, re_path

from ..views import FN026DetailView, FN026ListView, FN026SubspaceListView


PRJ_CD_REGEX = settings.PRJ_CD_URL_REGEX

urlpatterns = [
    path("fn026/", FN026ListView.as_view(), name="space_list"),
    path("<str:prj_cd>/spatial_strata", FN026ListView.as_view(), name="fn026-list"),
    path(
        "<str:prj_cd>/space/<str:space>",
        FN026DetailView.as_view(),
        name="fn026-detail",
    ),
    re_path(
        fr"fn026subspace/{PRJ_CD_REGEX}/(?P<space>[0-9a-zA-Z]{{1,4}})/",
        FN026SubspaceListView.as_view(),
        name="project_space_subspace_list",
    ),
    re_path(
        fr"fn026subspace/{PRJ_CD_REGEX}/",
        FN026SubspaceListView.as_view(),
        name="project_subspace_list",
    ),
    path("fn026subspace/", FN026SubspaceListView.as_view(), name="subspace_list"),
]
