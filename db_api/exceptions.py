from project_name.lib.exception_handler import APPException


class InvalidEmail(APPException):
    pass


class UserNotFound(APPException):
    message = "user not found"


class UserExistAlready(APPException):
    message = "user already exists"


class PasswordNotValid(APPException):
    message = "password not valid"