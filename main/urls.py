from django.urls import include, path
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("admin/", admin.site.urls),

    path("fn_portal/", include('fn_portal.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/fn_portal/', include('fn_portal.api.urls',
                                      namespace='fn_portal_api')),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
         path('__debug__/', include(debug_toolbar.urls)),
        # For django versions before 2.0:
        #url(r"^__debug__/", include(debug_toolbar.urls))
    ] + urlpatterns + static(settings.STATIC_URL,
                             document_root=settings.STATIC_ROOT)
