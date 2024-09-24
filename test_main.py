import pytest
from httpx import AsyncClient
from main import app  # Переконайтеся, що цей імпорт відповідає вашому модулю з додатком FastAPI

@pytest.mark.asyncio
async def test_get_posts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/posts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

from httpx import AsyncClient, ASGITransport

@pytest.mark.asyncio
async def test_create_post():
    new_post = {"title": "foo", "body": "bar", "userId": 1}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/posts", json=new_post)
    assert response.status_code == 200  # Якщо API повертає 200, змініть перевірку на 200
    assert response.json()["title"] == new_post["title"]

@pytest.mark.asyncio
async def test_update_post():
    updated_post = {"title": "foo updated", "body": "bar updated", "userId": 1}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put("/posts/1", json=updated_post)
    assert response.status_code == 200
    assert response.json()["title"] == updated_post["title"]

@pytest.mark.asyncio
async def test_delete_post():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/posts/1")
    assert response.status_code == 200
    assert response.json() == {"detail": "Post deleted successfully"}


@pytest.mark.asyncio
async def test_get_posts_error():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/nonexistent")
    assert response.status_code == 404



