from django.urls import path

from rest_framework import routers


from db_api.views import (
    LoginView
)


user_urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
]