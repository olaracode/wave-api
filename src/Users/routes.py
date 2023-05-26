from flask import Blueprint, request, jsonify
from src.Server.database import db
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from src.Helpers.handlers import error_handler
from .encrypt import generate_salt, generate_password, check_password
from .helpers import email_validator
from .models import User

user = Blueprint("users", __name__)


@user.route("/register", methods=["POST"])
def register_user():
    body = request.json
    name = body.get("name", None)
    email = body.get("email", None)
    password = body.get("password", None)
    if not name or not email or not password:
        return error_handler("All fields are required", 400)

    if not email_validator(email):
        return error_handler("Must be a valid email address", 500)

    user_exists = User.query.filter_by(email=email).one_or_none()
    if user_exists:
        return error_handler("Email in use", 405)

    salt = generate_salt()
    hashed_password = generate_password(password, salt)

    new_user = User(name=name, email=email, password=hashed_password, salt=salt)
    db.session.add(new_user)

    try:
        db.session.commit()
        user_object = {"id": new_user.id, "role": new_user.role.value}
        token = create_access_token(user_object)
        refresh_token = create_refresh_token(user_object)
        return (
            jsonify(
                {
                    "user": new_user.serialize(),
                    "token": token,
                    "refresh_token": refresh_token,
                }
            ),
            201,
        )

    except Exception as error:
        db.session.rollback()
        return error_handler(error.args, 500)


@user.route("/login", methods=["POST"])
def login_user():
    body = request.json
    email = body.get("email", None)
    password = body.get("password", None)
    if not email or not password:
        return error_handler("All fields are required", 400)

    user_exists = User.query.filter_by(email=email).one_or_none()
    if not user_exists:
        return error_handler("User not found", 404)

    if not check_password(user_exists.password, password, user_exists.salt):
        return error_handler("Password did not match", 401)
    user_object = {"id": user_exists.id, "role": user_exists.role.value}
    token = create_access_token(user_object)
    refresh_token = create_refresh_token(user_object)

    return jsonify({"token": token, "refresh_token": refresh_token}), 200


## token refresher


@user.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    user = get_jwt_identity()
    user_object = {"id": user.id, "role": user.role.value}
    token = create_access_token(user_object)
    refresh_token = create_refresh_token(user_object)

    return jsonify({"token": token, "refresh_token": refresh_token}), 200
