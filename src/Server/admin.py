from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from Server.database import db
from Users.models import User
from music.songs.models import Song
from music.comments.models import Comment
from music.projects.models import Project
from music.collaborators.models import Collaborator
import os


def create_admin(app):
    app.secret_key = os.environ.get("JWT_SECRET_KEY", "secret")

    admin = Admin(app, name="Spotifake Admin", template_mode="bootstrap3")

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Song, db.session))
    admin.add_view(ModelView(Comment, db.session))
    admin.add_view(ModelView(Project, db.session))
    admin.add_view(ModelView(Collaborator, db.session))
