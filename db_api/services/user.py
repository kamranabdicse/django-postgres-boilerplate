from db_api import crud
from db_api.exceptions import UserExistAlready, PasswordNotValid
from lib.validate_password import validate_password
from django.contrib.auth import authenticate
from lib.generate_jwt_token import generate_jwt_token
from django.contrib.auth.hashers import make_password


def login_user(username, password):
    user = authenticate(username=username, password=password)
    if not user:
        return None
    access = generate_jwt_token(username=username, id=user.id)
    return access


def register_user(username, password):
    if crud.user.get_by_username(username=username):
        raise UserExistAlready
    if not validate_password(password):
        raise PasswordNotValid
    
    user = crud.user.create(username=username, password=make_password(password))
    return user
