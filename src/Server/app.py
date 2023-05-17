from flask import Flask
from flask_jwt_extended import JWTManager
from .database import db, migrate
from .admin import create_admin
from .routes import api_routes_v1


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    api_routes_v1(app, prefix="/api/v1")
    create_admin(app)

    @app.route("/")
    def hello():
        """
        Simple endpoint for testing the server
        ---
        responses:
            200:
                description: A simple hello world
                type: string
        """
        return "<h1>Hello</h1>"

    return app
