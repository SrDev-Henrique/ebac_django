from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.post, name="home"),
]
