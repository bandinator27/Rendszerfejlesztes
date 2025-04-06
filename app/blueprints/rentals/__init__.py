from apiflask import APIBlueprint

rental_bp = APIBlueprint('rentals', __name__, tag="rentals")
from app.blueprints.rentals import routes