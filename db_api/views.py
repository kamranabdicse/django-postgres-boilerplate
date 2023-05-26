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
from db_api.exceptions import InvalidEmail , UserNotFound

from ninja import Router, Query
from db_api.services import (
    login_user,
    register_user
) 
from db_api.schema import (
    AuthenticationIn,
    AuthenticationOut,
    UserSchema,
)

router = Router()
logger = logging.getLogger(__name__)


@router.post(
    "login",
    response=AuthenticationOut,
)
def login(request, payload: AuthenticationIn):
    access = login_user(username=payload.username, password=payload.password)
    if not access:
        raise UserNotFound("user not found")
    return {"access": access}


@router.post(
    "register",
    response=UserSchema,
)
def register(request, payload: AuthenticationIn):
    user = register_user(username=payload.username, password=payload.password)
    if not user:
        raise UserNotFound("user not found")
    return user

