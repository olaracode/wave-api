from flask import Blueprint


def register_blueprint_with_prefix(app, blueprint, prefix):
    """
    Registers a blueprint with a prefix added to all routes.
    """
    url_prefix = f"/{prefix}" if prefix else ""
    app.register_blueprint(blueprint, url_prefix=url_prefix)


def register_blueprints(app, register, prefix=None):
    """
    Registers all blueprints with the app.
    """
    for blueprint in register:
        register_blueprint_with_prefix(app, blueprint, prefix)
