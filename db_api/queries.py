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
            return User( username= user_orm.username, pk= user_orm.pk)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create(username, password):
        user_orm = UserORM.objects.create(username=username, password=make_password(password))
        out = User(username=username, pk=user_orm.pk)
        return out