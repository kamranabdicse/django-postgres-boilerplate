from rest_framework import serializers, exceptions
from django.contrib.auth import authenticate, get_user_model

from db_api.lib.validate_phone_number import validate_phone_number
from db_api.models import UserORM

class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class GenerateOTPSerializer(serializers.Serializer):
    mobile = serializers.CharField(
        max_length=13,
        allow_null=False,
        allow_blank=False,
    )

    def validate_mobile(self, value):
        validated_phone_number = validate_phone_number(value)
        return validated_phone_number

class ValidateOTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(required=True, write_only=True)


class ValidateOTPResponseSerializer(serializers.Serializer):
    token = serializers.BooleanField(default=False)


class LoginSerializer(serializers.Serializer):
    username_field = get_user_model().USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        msg = "Invalid authentication"

        username = attrs.get("username", None)
        password = attrs.get("password", None)
        if (
            username or password
        ) is None:
            raise exceptions.AuthenticationFailed(msg)

        user = authenticate(username=username, password=password)
        if user is None:
            raise exceptions.AuthenticationFailed(msg)

        return attrs

    def to_representation(self, instance):
        response = super().to_representation(instance)
        username = response.pop("username")
        user = UserORM.objects.filter(username=username).first()
        access = user._generate_jwt_token()
        response["access"] = access
        return response

