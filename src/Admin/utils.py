from flask import request, jsonify
from src.Helpers.handlers import error_handler, serialize_array
from src.Server.database import db


def get_or_delete(id, model, model_name):
    user = model.query.get(id)
    if not user:
        return error_handler(f"{model_name} not found", 404)
    if request.method == "GET":
        return jsonify(user.serialize()), 200
    elif request.method == "DELETE":
        db.session.delete(user)
        try:
            db.session.commit()
            return jsonify(user.serialize()), 200
        except Exception as e:
            return error_handler(str(e), 500)


def paginate_model(model, model_name):
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    models = model.query.paginate(page=page, per_page=per_page)
    return jsonify({f"{model_name}": serialize_array(models.items), "info": ""}), 200
