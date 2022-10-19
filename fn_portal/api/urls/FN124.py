from django.urls import path

from ..views import LengthTallyList

urlpatterns = [
    path("fn124/", LengthTallyList.as_view(), name="fn124_list"),
]
