from apiflask import APIBlueprint
from app.database import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError
from functools import wraps

main_bp = APIBlueprint('main', __name__, tag="main")

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY']
        )
        if data["exp"] < int(datetime.now().timestamp()):
            return None
        return data
    except:
        return None
    
def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user = getattr(auth, "current_user", None)
            
            if not user or not user.get("roles"):
                raise HTTPError(message="Access denied", status_code=403)
            user_roles = user.get("roles", [])
            
            if any(role in user_roles for role in roles):
                return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper

from app.blueprints.user import user_bp
main_bp.register_blueprint(user_bp, url_prefix='/user')
from app.blueprints.cars import car_bp
main_bp.register_blueprint(car_bp, url_prefix='/car')
from app.blueprints.rentals import rental_bp
main_bp.register_blueprint(rental_bp, url_prefix='/rental')

from app.models import *
from app.main import routes