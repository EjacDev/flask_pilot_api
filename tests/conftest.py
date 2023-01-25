import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""

    # create the app with common test config
    app = create_app('TestingConfig')

    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class UserActions:
    def __init__(self, client):
        self._client = client

    def register(self, username="test", password="test"):
        return self._client.post(
            "/api/user/signup", data={
        "email": "example@gmail.com",
        "first_name": "example",
        "middle_name": "example",
        "last_name": "example",
        "password": "123456"
        }
        )

class ServiceActions:
    def __init__(self, client):
        self._client = client

    def create_service(self, username="test", password="test"):
        return self._client.post(
            "/api/service", data={
            "zipcode": "01027",
            "latitude": "",
            "longitude": "",
            "user_id": "1"
            }
        )

@pytest.fixture
def user(client):
    return UserActions(client)

@pytest.fixture
def service(client):
    return ServiceActions(client)