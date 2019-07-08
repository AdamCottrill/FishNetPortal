"""Urls for api endpoints for fn_portal

+ projects
+ <prj_cd>/sams
+ <prj_cd>/catcnts
+ <prj_cd>/biosamples

+ <prj_cd>/<sams>/<effs>

+ <prj_cd>/<sams>/<effs>/<spc>/<grp>/

"""

from django.conf.urls import url, include
from rest_framework import routers

from .views import FN011ViewSet

app_name = "fn_portal_api"

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register("project", FN011ViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [url(r"^", include(router.urls))]
