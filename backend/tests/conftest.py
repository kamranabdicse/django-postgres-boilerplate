import logging
import pytest
from rest_framework.test import APIClient
from .db_api.factories import UserFactory

LOGGER = logging.getLogger(__name__)


def pytest_collection_modifyitems(items):
    for item in items:
        item.add_marker('all')

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    "return User,Access"
    username = "test_user"
    user = UserFactory(username=username)
    return user

