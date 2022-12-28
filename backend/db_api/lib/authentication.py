import base64
import logging

import jwt

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import authentication, exceptions

from db_api.models import UserORM, BlacklistedToken


logger = logging.getLogger(__name__)


class CustomAuthentication(authentication.BaseAuthentication):
    msg = "Invalid authentication"
    authentication_header_prefix = ("Bearer", "Basic")

    def authenticate(self, request):
        """
        The `authenticate` method is called on every request regardless of
        whether the endpoint requires authentication.

        `authenticate` has two possible return values:

        1) `None` - We return `None` if we do not wish to authenticate. Usually
                    this means we know authentication will fail. An example of
                    this is when the request does not include a token in the
                    headers.

        2) `(user, token)` - We return a user/token combination when
                             authentication is successful.

                            If neither case is met, that means there's an error
                            and we do not return anything.
                            We simple raise the `AuthenticationFailed`
                            exception and let Django REST Framework
                            handle the rest.
        """
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            raise exceptions.AuthenticationFailed(self.msg)

        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix not in self.authentication_header_prefix:
            raise exceptions.AuthenticationFailed(self.msg)

        return self._authenticate_credentials(request, token, prefix)

    def _authenticate_credentials(self, request, token, prefix):

        blacklisted_token = BlacklistedToken.objects.filter(token=token).exists()
        if blacklisted_token:
            raise exceptions.AuthenticationFailed(self.msg)

        try:
            if prefix == "Bearer":
                decoded_token = jwt_decoder(token)
            else:
                decoded_token = basic_token_decoder(token)
                username = decoded_token.split(":")[0].strip()
                password = decoded_token.split(":")[1].strip()
                user = authenticate(username=username, password=password)
                if user is None:
                    raise Exception
        except Exception as e:
            raise exceptions.AuthenticationFailed(self.msg)

        try:
            if prefix == "Bearer":
                if "user_id" not in decoded_token.keys():
                    msg = "how the f*** did you get to this error message?!"
                    raise exceptions.AuthenticationFailed(msg)
                user = UserORM.objects.get(pk=decoded_token["user_id"])
            else:
                user = UserORM.objects.get(
                    username=decoded_token.split(":")[0].strip(),
                    can_use_basic_token=True,
                )
        except UserORM.DoesNotExist:
            raise exceptions.AuthenticationFailed(self.msg)

        if not user.is_active:
            raise exceptions.AuthenticationFailed(self.msg)

        return (user, token)


def jwt_decoder(token):
    decoded_jwt = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
    return decoded_jwt


def basic_token_decoder(token):
    decoded_basic_token = str(base64.b64decode(token), encoding="utf-8")
    return decoded_basic_token


def queryset_to_id_list(queryset):
    id_list = []
    for obj in queryset:
        id_list.append(obj.id)

    return id_list
