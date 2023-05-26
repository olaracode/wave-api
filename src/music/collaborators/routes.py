from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.Server.database import db
from src.Helpers.handlers import error_handler, serialize_array
from .models import Collaborator
from src.Music.projects.models import Project
from src.Users.models import User

collaborator = Blueprint("collaborators", __name__)


@collaborator.route("/", methods=["GET"])
def get_collaborators():
    collaborators = Collaborator.query.all()
    return jsonify(serialize_array(collaborators)), 200


@collaborator.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_project_collaborators(id):
    collaborators = Collaborator.query.filter_by(project_id=id).all()
    return jsonify(serialize_array(collaborators)), 200


@collaborator.route("/<int:id>/<int:user_id>", methods=["POST"])
@jwt_required()
def create_project_collaborator(id, user_id):
    if not user_id:
        return error_handler("Missing user_id parameter", 400)

    # check if the user exists
    user_exists = User.query.filter_by(id=user_id).first()
    if not user_exists:
        return error_handler("User not found", 404)

    # check if project exists and belongs to user
    user = get_jwt_identity()
    project = Project.query.filter_by(id=id, user_id=user["id"]).first()
    if not project:
        return error_handler("Project not found", 404)

    # check the collaborator already exists in the project
    collaborator = Collaborator.query.filter_by(user_id=user_id, project_id=id).first()
    if collaborator:
        return error_handler("Collaborator already exists", 400)

    # Create and save the collaborator
    new_collaborator = Collaborator(user_id=user_id, project_id=id)
    db.session.add(new_collaborator)

    try:
        db.session.commit()
        return jsonify(new_collaborator.serialize()), 201
    except Exception as e:
        return error_handler(str(e), 500)
