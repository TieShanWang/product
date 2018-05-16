
from django.conf.urls import url

from . import views

urlpatterns = [
    # mini program
    url(r'^miniupload', views.MiniApiView.as_view(), name='mini_upload'),
    url(r'^miniversion.json', views.mini_version, name='mini_version'),
    url(r'^miniinfo.json', views.mini_info, name='mini_info'),

]