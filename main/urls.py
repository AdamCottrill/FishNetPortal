from django.urls import include, path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from fn_portal.views import ProjectList

urlpatterns = [
    path("", view=ProjectList.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("fn_portal/", include("fn_portal.urls")),
    path("fn_portal/api/v1/", include("fn_portal.api.urls", namespace="fn_portal_api")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [path("__debug__/", include(debug_toolbar.urls))]
        + urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
