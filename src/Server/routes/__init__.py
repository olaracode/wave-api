from src.Users.routes import user
from src.Music.songs.routes import song
from src.Music.projects.routes import project
from src.Music.collaborators.routes import collaborator


def register_blueprint_with_prefix(app, blueprint, prefix):
    """
    Registers a blueprint with a prefix added to all routes.
    """
    url_prefix = f"/{prefix}" if prefix else ""
    app.register_blueprint(blueprint, url_prefix=url_prefix)


def api_routes_v1(app, prefix=None):
    register_blueprint_with_prefix(app, user, prefix + "/user")
    register_blueprint_with_prefix(app, song, prefix + "/song")
    register_blueprint_with_prefix(app, project, prefix + "/project")
    register_blueprint_with_prefix(app, collaborator, prefix + "/collaborator")
