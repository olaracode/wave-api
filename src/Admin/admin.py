from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)
from src.Users.encrypt import generate_password, check_password, generate_salt
from src.Users.models import User, roles
from src.Server.database import db
from src.Helpers.handlers import error_handler, serialize_array
from .middleware import admin_required
from .utils import get_or_delete, paginate_model

admin = Blueprint("admin", __name__)


@admin.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return error_handler("Missing JSON in request", 400)
    body = request.get_json()
    email = body.get("email")
    password = body.get("password")
    if not email:
        return error_handler("Missing email parameter", 400)
    if not password:
        return error_handler("Missing password parameter", 400)
    user = User.query.filter_by(email=email).first()
    if not user:
        return error_handler("User not found", 404)
    if not check_password(user.password, password, user.salt):
        return error_handler("Wrong password", 400)
    # create access token and refresh token
    print(user.role)
    if user.role != roles.admin:
        return error_handler("User is not admin", 400)
    jwt_user_object = {"id": user.id, "email": user.email, "is_admin": True}
    token = create_access_token(jwt_user_object)

    # Create a refresh token for the user.
    refresh_token = create_refresh_token(jwt_user_object)

    # Return the JWT token and the refresh token.
    return jsonify({"access_token": token, "refresh_token": refresh_token})


@admin.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return error_handler("Missing JSON in request", 400)
    body = request.get_json()
    email = body.get("email")
    name = body.get("name")

    password = body.get("password")
    if not email:
        return error_handler("Missing email parameter", 400)
    if not password:
        return error_handler("Missing password parameter", 400)
    user = User.query.filter_by(email=email).first()
    if user:
        return error_handler("User already exists", 400)
    salt = generate_salt()
    password = generate_password(password, salt)
    new_user = User(email=email, password=password, role="admin", name=name, salt=salt)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        return error_handler(str(e), 500)


@admin.route("/users", methods=["GET"])
@jwt_required()
@admin_required()
def get_all_users():
    # get all users with pagination, return the users as well as the pagination info
    return paginate_model(User, "Users")


@admin.route("/users/<int:user_id>", methods=["GET", "DELETE"])
@jwt_required()
@admin_required()
def user_by_id(user_id):
    return get_or_delete(user_id, User, "User")
