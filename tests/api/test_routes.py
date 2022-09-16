import pytest

from api.models import User


def create_user_data():
    return {
        "username": "mock username",
        "email": "mock email"
    }


def test_get_users(client, app_mixer):
    mock_user_data = create_user_data()
    user = app_mixer.blend(
        User,
        username=mock_user_data["username"],
        email=mock_user_data["email"],
    )

    response = client.get("/users")
    resp_users = response.json

    assert resp_users == [{
        "username": mock_user_data["username"],
        "email": mock_user_data["email"],
        "id": user.id
    }]


def test_create_user_endpoint_returns_expected_response_data(client):
    mock_user_data = create_user_data()

    response = client.post("/users/create", json=mock_user_data)
    response_data = response.json

    pytest.assume(response_data.get("email") == mock_user_data["email"])
    pytest.assume(response_data.get("username") == mock_user_data["username"])
    pytest.assume(type(response_data.get("id")) == int)


def test_create_user_endpoint_creates_user_in_db(client):
    mock_user_data = create_user_data()

    response = client.post("/users/create", json=mock_user_data)
    user_id = response.json["id"]

    queried_user = User.query.filter(User.id == user_id).first()

    pytest.assume(queried_user is not None)
    pytest.assume(queried_user.email == mock_user_data["email"])
    pytest.assume(queried_user.username == mock_user_data["username"])


def test_create_user_returns_400_status_when_missing_required_field(client):
    mock_user_data = create_user_data()
    mock_user_data.pop("email")

    response = client.post("/users/create", json=mock_user_data)

    assert response.status_code == 400


def test_create_user_returns_400_status_when_duplicate_user_data_provided(client, app_mixer):
    mock_user_data = create_user_data()
    _user = app_mixer.blend(
        User,
        username=mock_user_data["username"],
        email=mock_user_data["email"],
    )

    response = client.post("/users/create", json=mock_user_data)

    assert response.status_code == 400
