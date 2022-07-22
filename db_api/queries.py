from django.core.exceptions import ObjectDoesNotExist
from typing import Any, Dict, List, Optional, Union

from db_api.models import UserORM

class UserRecords:

    @staticmethod
    def get_by_username(username:str) -> Union[UserORM, bool]:
        try:
            user_orm = UserORM.objects.get(username=username)
            return user_orm
        except ObjectDoesNotExist:
            return None
