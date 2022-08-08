from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from typing import Any, Dict, List, Optional, Union
from db_api.models import UserORM
from modules.entities.user import User


class UserRecords:
    @staticmethod
    def get_by_username(username: str) -> Optional[UserORM]:
        try:
            user_orm = UserORM.objects.get(username=username)
            user = User( username= user_orm.username)
            user.id = user_orm.id
            return user
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(username, password):
        out = User(username=username)
        user_orm = UserORM.objects.create(username=username, password=make_password(password))
        out.id = user_orm.id
        return out