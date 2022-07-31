from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from db_api.queries import UserRecords
from django.contrib.auth.password_validation import validate_password
from django.db import transaction

from db_api.models import UserORM
from project_name.lib.logger import logger


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("style", {})

        kwargs["style"]["input_type"] = "password"
        kwargs["write_only"] = True

        super().__init__(*args, **kwargs)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = PasswordField()

    def validate(self, attrs):
        msg = "Invalid authentication"

        username = attrs.get("username", None)
        password = attrs.get("password", None)
        if not (username and password):
            raise exceptions.AuthenticationFailed(msg)

        user = authenticate(username=username, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed(msg)

        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        username = response.pop("username")
        user = UserRecords.get_by_username(username=username)
        access = user._generate_jwt_token()
        response["access"] = access
        return response


class RegisterSerilizer(serializers.Serializer):
    username = serializers.EmailField(
        required=True,
        # validators=[UniqueValidator(queryset=User.objects.all())],
        write_only=True,
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            validate_password
        ],  # TODO in order to error handeling its better to handle it on handle method
    )

    def validate(self, attrs):
        username = attrs.get("username")
        if UserORM.objects.filter(username=username).exists():
            raise exceptions.ValidationError("This username is exists already")
        return attrs

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user_data = {
                    "username": validated_data.get("username"),
                    "password": make_password(validated_data.get("password")),
                }
                user_orm = UserORM.objects.create(**user_data)
                return user_orm

        except Exception as err:
            logger.error("in user registration something went wrong!")
            raise err
