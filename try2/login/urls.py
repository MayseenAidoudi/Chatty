from django.urls import path

from . import views

app_name = "login"

urlpatterns = [
    path("chat/", views.handler, name="handler"),
    path("chat/logout/", views.logout_user, name="logout_user"),
    path("chat/<str:username_link>/", views.messaging_service, name="handler_user_included"),
    path("register/", views.register_user, name="register")
]