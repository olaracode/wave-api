from flask import Flask
from flask_jwt_extended import JWTManager
from .database import db, migrate
from .routes import api_routes_v1
from src.Admin.admin import admin
from flask_cors import CORS
import os


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")
    app.secret_key = os.environ.get("JWT_SECRET_KEY")
    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)
    app.register_blueprint(admin, url_prefix="/admin")
    api_routes_v1(app, prefix="/api/v1")

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

