from django.urls import path

from ..views import FN012ListView, FN012ProtocolListView


urlpatterns = [
    path("fn012/", FN012ListView.as_view(), name="sample_specs_list"),
    path(
        "fn012_protocol/",
        FN012ProtocolListView.as_view(),
        name="protocol_sample_specs_list",
    ),
]
