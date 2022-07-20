from rest_framework.mixins import RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.schemas.openapi import AutoSchema, SchemaGenerator
import yaml


class CustomAPIView(APIView):
    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


def is_list_view(path, method, view):
    """
    Return True if the given path/method appears to represent a list view.
    """
    if hasattr(view, "action"):
        # Viewsets have an explicitly defined action, which we can inspect.
        return view.action == "list"

    if method.lower() != "get":
        return False
    if isinstance(view, RetrieveModelMixin):
        return False
    path_components = path.strip("/").split("/")
    if path_components and "{" in path_components[-1]:
        return False
    return True


class CustomSchemaGenerator(SchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request=request, public=public)
        bearer_security_schema = {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "description": """
                    This API uses bearer token authorization,
                    Use login, signin services to get access token,
                    Enter access token here
                """,
            },
        }
        schema["security"] = [bearer_security_schema]
        schema["components"]["securitySchemes"] = bearer_security_schema
        return schema


class CustomSchema(AutoSchema):
    def __init__(self, **kwargs):
        self.extra_info = kwargs.pop("extra_info")
        super().__init__(**kwargs)

    @property
    def documentation(self):
        if not hasattr(self, "_documentation"):
            if self.view.__doc__:
                try:
                    self._documentation = yaml.safe_load(self.view.__doc__)
                except yaml.scanner.ScannerError:
                    self._documentation = {}
            else:
                self._documentation = {}
        return self._documentation

    def get_operation(self, path, method):

        operation = super().get_operation(path, method)

        operation["responses"] = self.get_responses(path, method)

        doc_operation = self.documentation.get(method.lower(), {})
        operation.update(doc_operation)

        return operation

    def get_request_serializer(self, path, method):
        """
        Override this method if your view uses a different serializer for
        handling request body.
        """
        return self.extra_info.get("serializer")

    def get_request_body(self, path, method):
        if method not in ("PUT", "PATCH", "POST"):
            return {}

        self.request_media_types = self.map_parsers(path, method)

        serializer = self.get_request_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)

        return {
            "content": {ct: {"schema": item_schema} for ct in self.request_media_types}
        }

    def get_responses(self, path, method):
        if method == "DELETE":
            return {"204": {"description": ""}}

        self.response_media_types = self.map_renderers(path, method)

        serializer = self.extra_info.get("response_serializer")
        if not serializer:
            serializer = self.get_request_serializer(path, method)

        if not isinstance(serializer, serializers.Serializer):
            item_schema = {}
        else:
            item_schema = self._get_reference(serializer)

        is_list = self.extra_info.get("is_list")
        if not is_list:
            is_list = is_list_view(path, method, self.view)
        if is_list:
            response_schema = {
                "type": "array",
                "items": item_schema,
            }
            paginator = self.get_paginator()
            if paginator:
                response_schema = paginator.get_paginated_response_schema(
                    response_schema
                )
        else:
            response_schema = item_schema
        status_code = "200"
        return {
            status_code: {
                "content": {
                    ct: {"schema": response_schema} for ct in self.response_media_types
                },
                # description is a mandatory property,
                # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#responseObject
                "description": "",
            }
        }

    def get_components(self, path, method):
        if method.lower() == "delete":
            return {}

        request_serializer = self.get_request_serializer(path, method)

        components = {}

        if isinstance(request_serializer, serializers.Serializer):
            component_name = super().get_component_name(request_serializer)
            content = super().map_serializer(request_serializer)
            components.setdefault(component_name, content)

        response_serializer = self.extra_info.get("response_serializer")

        if isinstance(response_serializer, serializers.Serializer):
            component_name = super().get_component_name(response_serializer)
            content = super().map_serializer(response_serializer)
            components.setdefault(component_name, content)

        doc_components = self.documentation.get("components", {})
        components.update(doc_components)

        return components
