from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.project_list, name='project_list'),

    url(r'^api/catcnts/(?P<slug>[a-z]{3}_[a-z]{2}\d{2}_([a-z]|\d){3})/$',
    views.project_catch_counts_json,
    name='project_catch_counts_json'),


    url(r'^api/catcnts/(?P<slug>[a-z]{3}_[a-z]{2}\d{2}_([a-z]|\d){3})/(?P<sam>[\w-]+)/$',
    views.sample_catch_counts_json,
    name='sample_catch_counts_json'),



    url(r'^catcnts/(?P<prj_cd>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$',
    views.project_catch_counts,
    name='project_catch_counts'),

    url(r'^project_detail/(?P<slug>[a-z]{3}_[a-z]{2}\d{2}_([a-z]|\d){3})/$',
    views.project_detail,
    name='project_detail'),

    url(r'^sample_detail/(?P<slug>[a-z]{3}_[a-z]{2}\d{2}_([a-z]|\d){3})/(?P<sam>[\w-]+)/$',
    views.sample_detail,
    name='sample_detail'),



]
