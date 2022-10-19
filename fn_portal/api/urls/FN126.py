from django.urls import path

from ..views import FN126ReadOnlyList

urlpatterns = [
    path("fn126/", FN126ReadOnlyList.as_view(), name="fn126_list"),
]
