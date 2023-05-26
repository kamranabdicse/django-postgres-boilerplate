from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from project_name.lib.openapi_v2 import app_api
# from project_name.router import url_patterns as router


from db_api.views import router as user_router

app_api.add_router("v1/user/", user_router, tags=["users"])

urlpatterns = [
    path('admin/', admin.site.urls),
    # path(
    #     "api/openapi/",
    #     get_schema_view(
    #         title="API Services",
    #         description="API developers hoping to use our service",
    #         generator_class=CustomSchemaGenerator,
    #         public=True,
    #     ),
    #     name="openapi-schema",
    # ),
    # path(
    #     "api/docs/",
    #     TemplateView.as_view(
    #         template_name="swagg.html", extra_context={"schema_url": "openapi-schema"}
    #     ),
    #     name="docs",
    # ),
    path("api/", app_api.urls),
]
