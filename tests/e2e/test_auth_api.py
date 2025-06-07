import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from src.bootstrap.main import app
import os
import sys
from typing import AsyncGenerator, Generator


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(transport=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_register_user(client):
    response = client.post(
        "/auth/users",
        json={
            "login": "testuser",
            "password": "testpassword",
            "email": "test@example.com"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user(client):
    client.post(
        "/auth/users",
        json={
            "login": "testuser2",
            "password": "testpassword",
            "email": "test2@example.com"
        }
    )
    
    response = client.post(
        "/auth/token",
        json={
            "login": "testuser2",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/token",
        json={
            "login": "nonexistentuser",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    data = response.json()
    assert "Invalid credentials" in data["detail"]
