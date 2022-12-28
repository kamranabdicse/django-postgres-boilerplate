import factory
from db_api.models import UserORM

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'db_api.UserORM'
        django_get_or_create = ("username")
    
    first_name = ""
    last_name = ""
    password = "test_user_123456"
    username = "test_user_factory@examle.com"
    email = "test_user_factory@examle.com"
    is_active = True