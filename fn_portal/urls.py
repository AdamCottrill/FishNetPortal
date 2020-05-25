from django.urls import path

from .views import (
    ProjectList,
    project_detail,
    sample_detail,
    project_spc_biodata,
    project_catch_over_time,
    gear_list,
    gear_detail,
    edit_gear,
    edit_subgear,
    project_catch_counts2_json,
    project_catch_counts_json,
    project_spc_biodata_json,
    project_catch_over_time_json,
    sample_catch_counts_json,
)

app_name = "fn_portal"

urlpatterns = [
    path("", view=ProjectList.as_view(), name="project_list"),
    path("project_detail/<slug:slug>/", view=project_detail, name="project_detail"),
    path(
        "sample_detail/<slug:slug>/<str:sam>/", view=sample_detail, name="sample_detail"
    ),
    # re_paths for  biodata for a particular species and project
    path(
        "biodata/<slug:slug>/<str:spc>/",
        view=project_spc_biodata,
        name="project_spc_biodata",
    ),
    # re_paths for catch-counts through time for projects with matching prj_cd
    path(
        "catch_over_time/<slug:slug>/",
        view=project_catch_over_time,
        name="project_catch_over_time",
    ),
    # =============================================
    #                GEAR
    path("gears/<str:username>/", view=gear_list, name="gears_assigned_to"),
    path("gears/", view=gear_list, name="gear_list"),
    path("gears/gear_detail/<str:gear_code>)/", view=gear_detail, name="gear_detail"),
    path("gears/edit_gear/<str:gear_code>/", view=edit_gear, name="edit_gear"),
    path(
        "gears/edit_subgear/<str:gear_code>/<str:eff>/",
        view=edit_subgear,
        name="edit_subgear",
    ),
    # =============================================
    #  API VIEWS / AJAX endpoints used in templates
    # my attempt to get all of the catch count data in its lowest form
    # (catch by effort by species) and analyze it with server side js.
    path(
        "api/catcnts2/<slug:slug>/",
        view=project_catch_counts2_json,
        name="project_catch_counts2_json",
    ),
    # this url is a copy of catch_counts2 - follows the convention of
    # accesing the data using view-api pattern.
    path(
        "api/project_detail/<slug:slug>/",
        view=project_catch_counts2_json,
        name="project_detail_json",
    ),
    path(
        "api/catcnts/<slug:slug>/<str:sam>/",
        view=sample_catch_counts_json,
        name="sample_catch_counts_json",
    ),
    # this url is a copy of sample_catch_counts - follows the convention of
    # accesing the data using view-api pattern.
    path(
        "api/sample_detail/<slug:slug>/<str:sam>/",
        view=sample_catch_counts_json,
        name="sample_detail_json",
    ),
    path(
        "api/catcnts/<slug:slug>/",
        view=project_catch_counts_json,
        name="project_catch_counts_json",
    ),
    path(
        "api/biodata/(<slug:slug>/<str:spc>/",
        view=project_spc_biodata_json,
        name="project_spc_biodata_json",
    ),
    path(
        "api/catch_over_time/<slug:slug>/",
        view=project_catch_over_time_json,
        name="project_catch_over_time_json",
    ),
]
