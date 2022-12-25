import logging
import random
from rest_framework.exceptions import NotFound, ValidationError, APIException
from django.http import JsonResponse, Http404
from rest_framework.schemas.openapi import AutoSchema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, schema
from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus


from db_api.serializers import LoginSerializer
from db_api.serializers import RegisterSerilizer
from lib.exceptions.exception import InvalidEmail


logger = logging.getLogger(__name__)


def wrap_exceptions(func):
    def func_(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except InvalidEmail:
            raise ValidationError("Field username must be valid email")
    return func_


class LoginView(generics.GenericAPIView):
    """
    Login
    """
    schema = AutoSchema(tags=["user"], operation_id_base="login")
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @wrap_exceptions
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return JsonResponse(serializer.data, safe=False)


class RegisterView(generics.GenericAPIView):
    schema = AutoSchema(tags=["user"], operation_id_base="register")
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerilizer

    @wrap_exceptions
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)
