from django.urls import path

from rest_framework import routers


from db_api.views import (
    generate_otp,
    LoginView
)


user_urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("generate-otp", generate_otp),
    # path("otp-validation", otp_validation),
]