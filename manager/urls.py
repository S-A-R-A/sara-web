from django.conf.urls import include, url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.show_timetabling),
    url(r'^timetabling/(?P<dayid>\d+)/(?P<periodid>\d+)/(?P<areaid>\d+)', views.show_timetabling),
    url(r'^timetabling/(?P<dayid>\d+)/(?P<periodid>\d+)', views.show_timetabling),
    url(r'^timetabling/(?P<dayid>\d+)', views.show_timetabling),
    url(r'^timetabling', views.show_timetabling),
]
