
from django.urls import path, re_path

from navigation import views


urlpatterns = [
    path('', views.base),
    re_path(r'^(?P<path>(([\w\s]+/)*))$', views.go),
    re_path(r'^(?P<path>(([\w\s]+/)*[\w\s.]+))$', views.open)
]
