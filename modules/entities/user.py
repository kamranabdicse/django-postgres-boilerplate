from utils.generate_jwt_token import generate_jwt_token
from utils.validate_email import validate_email


class InvalidEmail(Exception):
    def __init__(self, message, errors):            
        super().__init__(message)        
        self.errors = errors

class User:
    """
    here is the business logic of user entity
    """
    def __init__(self, username, pk):
        if not validate_email(username):
            raise InvalidEmail
        self.pk = pk
        self.username = username
        self.token = generate_jwt_token(username=self.username, pk=self.pk)

