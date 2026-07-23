from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.post, name="home"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
]
