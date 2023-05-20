from flask import Blueprint, request, jsonify
from firebase import firebase_bucket
from Helpers.handlers import error_handler
from .models import Song
from Music.projects.models import Project
from Server.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity

song = Blueprint("songs", __name__)


@song.route("/", methods=["GET"])
def get_music():
    songs = Song.query.all()
    return jsonify([song.serialize() for song in songs]), 200


@song.route("/<int:project_id>", methods=["POST"])
@jwt_required()
def post_music(project_id):
    form = request.form
    files = request.files
    if not form:
        return error_handler("No form data", 400)
    name = form.get("name")
    if not name:
        return error_handler("Missing name", 400)
    song = files.get("song")
    image = files.get("image")
    if not song or not image:
        return error_handler("Song and cover image are required", 400)
    # check if file is audio
    print(song.filename.endswith(".mp3"))
    if not song.filename.endswith(".mp3") and not song.filename.endswith(".wav"):
        return error_handler("File is not audio", 400)

    project = Project.query.get(project_id)
    if not project:
        return error_handler("Project not found", 404)
    if not name:
        return error_handler("Missing name", 400)
    version = len(project.songs) + 1
    name = name + f"-{version}"
    # Upload song to firebase storage
    try:
        song_url = firebase_bucket.upload_file(song, name)
        image_url = firebase_bucket.upload_file(image, name + "-cover")
        if not song_url:
            return error_handler("Error uploading song", 500)
        new_song = Song(
            name=name,
            version=version,
            project_id=project_id,
            song_url=song_url,
            img_url=image_url,
            user_id=get_jwt_identity().get("id"),
        )
        db.session.add(new_song)
        db.session.commit()
        return jsonify(new_song.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return error_handler(str(e), 500)


@song.route("/music/<id>", methods=["DELETE"])
@jwt_required()
def delete_music(id):
    # Get the music document from Firestore
    song = Song.query.get(id)
    if not song:
        return error_handler("Music not found", 404)

    if song.user_id != get_jwt_identity().get("id"):
        return error_handler("Unauthorized", 401)

    # Delete the music document
    file_path = song.url.split(firebase_bucket.name + "/")[1]
    db.session.delete(song)
    db.session.commit()

    # Delete the music file from Firebase Storage
    firebase_bucket.delete_file(file_path)

    return jsonify({"message": "Music deleted"}), 200
