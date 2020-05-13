
from django.urls import path, re_path

from navigation import views


urlpatterns = [
    re_path(r'^(?P<path>(([\w\s]+/)*))$', views.go),
    re_path(r'^(?P<path>(([\w\s]+/)*[\w\s.]+))$', views.open)
]
