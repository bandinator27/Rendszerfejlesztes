from apiflask import APIBlueprint

car_bp = APIBlueprint('car', __name__, tag="car")
from app.blueprints.cars import routes