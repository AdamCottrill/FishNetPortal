from django.urls import include, path
from django.contrib import admin

# from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_swagger.views import get_swagger_view

from django.conf import settings
from django.conf.urls.static import static

API_TITLE = "Fishnet Portal API"
API_DESC = "A Restful API for your Fishnet-II Data"
schema_view = get_swagger_view(title=API_TITLE)

from fn_portal.views import ProjectList

urlpatterns = [
    path("", view=ProjectList.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("fn_portal/", include("fn_portal.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/fn_portal/", include("fn_portal.api.urls", namespace="fn_portal_api")),
    # api documentation
    path("docs/", include_docs_urls(title=API_TITLE, description=API_DESC)),
    # path("schema/", schema_view),
    path("swagger-docs/", schema_view),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [path("__debug__/", include(debug_toolbar.urls))]
        + urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
