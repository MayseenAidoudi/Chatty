from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path("", views.handler, name="handler"),
    path("logout/", views.logout_user, name="logout_user"),
]