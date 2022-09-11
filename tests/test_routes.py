import pytest

from api.models import User


def test_get_users(client, app_mixer):
    username = "mock username"
    email = "mock email"
    user = app_mixer.blend(User, username=username, email=email)

    response = client.get("/users")
    resp_users = response.json

    assert resp_users == [{"username": username, "email": email, "id": user.id}]


def test_create_user_endpoint_creates_user(client):
    username = "mock username"
    email = "mock email"
    request_data = {
        "email": email,
        "username": username,
    }

    response = client.post("/users/create", json=request_data)
    response_data = response.json

    # assert all((
    #     type(response_data.get("id")) == int,
    #     response_data.get("email") == email,
    #     response_data.get("username") == username,
    # ))
    pytest.assume(response_data.get("email") == email)
    pytest.assume(response_data.get("username") == username)
    pytest.assume(type(response_data.get("id")) == int)


"""
TODO
Future Tests:
    - /users/create should return a 400 status_code when request missing required fields
    - /users/create should return a 400 status_code when duplicate user data provided
"""
