from django.urls import path, include
from db_api.urls import user_urlpatterns as user


url_patterns = [
    path("v1/user/", include(user)),
]

