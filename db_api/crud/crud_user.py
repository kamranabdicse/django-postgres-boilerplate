from db_api.models import UserORM
from typing import Optional
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from lib.generate_jwt_token import generate_jwt_token


class CRUDUser:
    @staticmethod
    def get_by_username(username: str) -> Optional[UserORM]:
        try:
            return UserORM.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def authentication(username: str, password: str) -> str:
        user = authenticate(username=username, password=password)
        if not user:
            return None
        access = generate_jwt_token(username=username, id=user.id)
        return access
    
    @staticmethod
    def create(**kwargs):
        return UserORM.objects.create(**kwargs)


user = CRUDUser()