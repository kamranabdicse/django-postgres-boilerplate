import json
import pytest
import logging
from rest_framework.test import APIClient
from db_api.models import UserORM

LOGGER = logging.getLogger(__name__)

class TestUserEndpoints:
    endpoint = "/api/v1/user/"

    @pytest.mark.db_api
    @pytest.mark.e2e
    @pytest.mark.django_db(databases=["default"])
    def test_user_login(self, api_client: APIClient):
        UserORM.objects.create_user(username='user1@example.com',
                                 password='kamran123')

        data = {"username": "user1@example.com", "password": "kamran123"}
        response = api_client.post(path=f"{self.endpoint}login", data=data)

        assert response.status_code == 200
        assert "access" in json.loads(response.content)

    @pytest.mark.db_api
    @pytest.mark.e2e
    @pytest.mark.django_db(databases=["default"])
    def dtest_user_user_register(
        self, user: UserORM, api_client: APIClient
    ):
        data = {"username": "testusername@gmail.com", "password": "aA12345678"}

        response = api_client.post(path=f"{self.endpoint}register", data=data)

        print(response.content)

        assert response.status_code == 200
