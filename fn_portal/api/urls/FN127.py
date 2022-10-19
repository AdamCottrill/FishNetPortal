from django.urls import path

from ..views import FN127ReadOnlyList

urlpatterns = [
    path("fn127/", FN127ReadOnlyList.as_view(), name="fn127_list"),
]
