from flask import request
from flask_jwt_extended import get_jwt_identity
from functools import wraps


def admin_required():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = get_jwt_identity()
            print(user)
            if not user["is_admin"]:
                return {"message": "Admins only!"}, 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
