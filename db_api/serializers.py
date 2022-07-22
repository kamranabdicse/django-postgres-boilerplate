from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, get_user_model

from db_api.lib.validate_phone_number import validate_phone_number
from db_api.queries import UserRecords


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
