from apiflask import APIBlueprint

main_bp = APIBlueprint('main', __name__, tag="main")

from app.main import routes
from app.models import *