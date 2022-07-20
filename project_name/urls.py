"""project_name URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

from project_name.lib.openapi import CustomSchemaGenerator
from project_name.router import url_patterns as router

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        "api/openapi/",
        get_schema_view(
            title="API Services",
            description="API developers hoping to use our service",
            generator_class=CustomSchemaGenerator,
            public=True,
        ),
        name="openapi-schema",
    ),
    path(
        "api/docs/",
        TemplateView.as_view(
            template_name="swagg.html", extra_context={"schema_url": "openapi-schema"}
        ),
        name="docs",
    ),
    path("api/", include(router)),
]
