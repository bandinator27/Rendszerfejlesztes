from apiflask import APIBlueprint

car_bp = APIBlueprint('cars', __name__, tag="cars")
from app.blueprints.cars import routes