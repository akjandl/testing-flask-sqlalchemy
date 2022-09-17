from flask import Blueprint, request

from db import db
from api.models.user import User


routes_blueprint = Blueprint("routes", __name__)


@routes_blueprint.route("/users", methods=["GET"])
def users():
    all_users = User.query.all()
    users_data = [{"id": u.id, "username": u.username, "email": u.email} for u in all_users]
    return users_data, 200


@routes_blueprint.route("/users/create", methods=["POST"])
def create_user():
    data = request.json
    if not data:
        return {"msg": "Request body could not be parsed as JSON"}, 400

    username = data.get("username")
    email = data.get("email")
    response_content = {"username": username, "email": email}
    if not all((username, email)):
        return {"msg": f"Username and email required. Received: {response_content}"}, 400

    existing_user = User.query.filter(
        (User.username == username) | (User.email == email),
    ).first()
    if existing_user:
        return {"msg": "Username or email already used"}, 400

    user = User(email=email, username=username)
    db.session.add(user)
    db.session.commit()

    return {**response_content, "id": user.id}, 201
