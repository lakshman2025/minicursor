from fastapi.testclient import TestClient

from app.api import todo_routes
from app.main import app


client = TestClient(app)


def setup_function():
    todo_routes._todos.clear()
    todo_routes._next_id = 1


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_list_get_update_and_delete_todo():
    create_response = client.post(
        "/todos",
        json={"title": "Buy milk", "description": "2 liters", "completed": False},
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created == {
        "id": 1,
        "title": "Buy milk",
        "description": "2 liters",
        "completed": False,
    }

    list_response = client.get("/todos")
    assert list_response.status_code == 200
    assert list_response.json() == [created]

    get_response = client.get("/todos/1")
    assert get_response.status_code == 200
    assert get_response.json() == created

    update_response = client.patch("/todos/1", json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    delete_response = client.delete("/todos/1")
    assert delete_response.status_code == 204

    missing_response = client.get("/todos/1")
    assert missing_response.status_code == 404
