from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Project
from Server.database import db
from Helpers.handlers import error_handler, serialize_array

project = Blueprint("projects", __name__)


@project.route("/", methods=["GET"])
@jwt_required()
def get_projects():
    user = get_jwt_identity()
    projects = Project.query.filter_by(user_id=user["id"]).all()
    return jsonify(serialize_array(projects)), 200


@project.route("/", methods=["POST"])
@jwt_required()
def create_project():
    if not request.is_json:
        return error_handler("Missing JSON in request", 400)
    body = request.get_json()
    name = body.get("name")
    if not name:
        return error_handler("Missing name parameter", 400)
    user = get_jwt_identity()
    # check if it already exists
    project = Project.query.filter_by(name=name, user_id=user["id"]).all()
    if project:
        version = len(project) + 1
    else:
        version = 1
    new_project = Project(name=name, user_id=user["id"], version=version)
    db.session.add(new_project)
    try:
        db.session.commit()
        return jsonify(new_project.serialize()), 201
    except Exception as e:
        return error_handler(str(e), 500)
