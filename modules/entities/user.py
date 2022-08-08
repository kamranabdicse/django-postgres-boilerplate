from lib.generate_jwt_token import generate_jwt_token
from lib.validate_email import validate_email


class InvalidEmail(Exception):
    def __init__(self, message, errors):            
        super().__init__(message)        
        self.errors = errors

class User:
    """
    here is the business logic of user entity
    """
    def __init__(self, username):
        if not validate_email(username):
            raise InvalidEmail
        self.username = username
        
    def get_token(self):    
        self.token = generate_jwt_token(username=self.username, id=self.id)
        return self.token

    def set_id(self, id):
        self.__id=id
    
    def get_id(self):
        return self.__id