from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.show_timetabling),
    url(r'^timetabling/(?P<dayid>\d+)', views.show_timetabling),
    url(r'^timetabling/(?P<dayid>\d+)/(?P<periodid>\d+)', views.show_timetabling),
]
