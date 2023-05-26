from typing import Optional
from ninja import ModelSchema, Schema
from db_api.models import UserORM


class UserSchema(ModelSchema):
    class Config:
        model = UserORM
        model_fields = ["first_name"]


class AuthenticationIn(Schema):
    username: str
    password: str


class AuthenticationOut(Schema):
    access: str

    
