from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r"^fn_portal/", include("fn_portal.urls")),
    url(r"^admin/", include(admin.site.urls)),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        # path('__debug__/', include(debug_toolbar.urls)),
        # For django versions before 2.0:
        url(r"^__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns + static(settings.STATIC_URL,
                             document_root=settings.STATIC_ROOT)
