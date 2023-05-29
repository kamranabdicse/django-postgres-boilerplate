from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

# from project_name.lib.openapi_v2 import app_api
# from project_name.router import url_patterns as router


# from db_api.views import router as user_router

# app_api.add_router("v1/user/", user_router, tags=["users"])
from .api import api

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls)
    # path("api/", app_api.urls),
]
