import logging
import random

from django.http import JsonResponse, Http404
from rest_framework.schemas.openapi import AutoSchema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, schema


from db_api.serializers import LoginSerializer


logger = logging.getLogger(__name__)


class LoginView(generics.GenericAPIView):
    """
    Login
    """

    schema = AutoSchema(tags=["user"], operation_id_base="login")
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, safe=False)
