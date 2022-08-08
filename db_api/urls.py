from django.urls import path

from rest_framework import routers


from db_api.views import (
    LoginView,
    RegisterView,
)


user_urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("register", RegisterView.as_view(), name="register"),
]