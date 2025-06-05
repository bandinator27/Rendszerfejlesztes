from apiflask import APIBlueprint
from app.extensions import auth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime
from apiflask import HTTPError, HTTPTokenAuth
from functools import wraps
from app.models.users import Users

main_bp = APIBlueprint('main', __name__, tag="main")

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'])
        user_id = data.get("sub")
        if user_id:
            user = Users.query.get(user_id)
            if user:
                return user
        return None

    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None
    except Exception as e:
        print(f"An error occurred during token verification: {e}")
        return None

# @auth.verify_token
# def verify_token(token):
#     try:
#         data = jwt.decode(
#             token.encode('ascii'),
#             current_app.config['SECRET_KEY']
#         )
#         if data["exp"] < int(datetime.now().timestamp()):
#             return None
#         return data
#     except:
#         return None
    
def role_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles")]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)        
            raise HTTPError(message="Access denied! (role_required)", status_code=403)
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