"""Urls for api endpoints for some common lists that our users will need.

"""

from django.conf import settings
from django.urls import path, re_path

from ..views import (
    FNProtocolListView,
    GearEffortProcessTypeListView,
    GearListView,
    LakeExtentListView,
    ProjectLeadListView,
    SpeciesListView,
    project_wizard,
)

# from rest_framework import routers


PRJ_CD_REGEX = settings.PRJ_CD_URL_REGEX


urlpatterns = [
    # path("", include(router.urls)),
    # =========================
    # READONLY ListViews:
    path("species_list/", SpeciesListView.as_view(), name="species_list"),
    path("prj_ldr/", ProjectLeadListView.as_view(), name="project_lead_list"),
    path("gear/", GearListView.as_view(), name="gear_list"),
    path(
        "gear_effort_process_types/",
        GearEffortProcessTypeListView.as_view(),
        name="gear_eff_process_types_list",
    ),
    path("lakes/", LakeExtentListView.as_view(), name="lake_extent_list"),
    path("protocols/", FNProtocolListView.as_view(), name="protocol_list"),
    path("project_wizard/", project_wizard, name="project_wizard"),
]
