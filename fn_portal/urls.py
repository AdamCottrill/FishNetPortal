from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .api.urls import urlpatterns as api_urls
from .views import (ProjectList, edit_gear, edit_subgear, gear_detail,
                    gear_list, project_catch_counts_json,
                    project_catch_over_time, project_catch_over_time_json,
                    project_data_upload, project_detail, project_spc_biodata,
                    project_spc_biodata_json, sample_catch_counts_json,
                    sample_detail)

# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls
# from rest_framework_swagger.views import get_swagger_view





API_TITLE = "Fishnet Portal API"
API_DESC = "A Restful API for your Fishnet-II Data"


app_name = "fn_portal"

urlpatterns = [
    path("", view=ProjectList.as_view(), name="project_list"),
    # =============================================
    #               PROJECT VIEWS
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

    path("project_data_upload/", view=project_data_upload, name="upload_project_data"),


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
        view=project_catch_counts_json,
        name="project_catch_counts_json",
    ),
    # this url is a copy of catch_counts - follows the convention of
    # accesing the data using view-api pattern.
    path(
        "api/project_detail/<slug:slug>/",
        view=project_catch_counts_json,
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


schema_view = get_schema_view(
    openapi.Info(
        title=API_TITLE,
        default_version="v1",
        description=API_DESC,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="adam.cottrill@ontario.ca"),
        license=openapi.License(name="BSD License"),
    ),
    # generate docs for all endpoint from here down:
    patterns=urlpatterns + api_urls,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    # =============================================
    #          API AND DOCUMENTATION
    # api documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
