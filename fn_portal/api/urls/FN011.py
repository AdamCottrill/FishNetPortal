from django.urls import path

from ..views import FN011DetailView, FN011ListView


urlpatterns = [
    path("fn011/", FN011ListView.as_view(), name="project_list"),
    path("fn011/<slug:slug>/", FN011DetailView.as_view(), name="project_detail"),
]
