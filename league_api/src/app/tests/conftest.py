from fastapi.testclient import TestClient
import pytest_asyncio

from app.main import get_settings, app

settings = get_settings()


class AuthTestClient(TestClient):
    def post(self, *args, **kwargs):
        self.headers.update({'Authorization': f"Bearer {settings.API_KEY}"})
        return super().post(*args, **kwargs)


@pytest_asyncio.fixture
def client():
    with AuthTestClient(app) as c:
        yield c
