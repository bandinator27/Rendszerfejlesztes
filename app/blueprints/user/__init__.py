from apiflask import APIBlueprint

user_bp = APIBlueprint('user', __name__, tag="user")
from app.blueprints.user import routes