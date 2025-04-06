from app.blueprints.rentals import rental_bp
from app.blueprints.rentals.schemas import RentalsResponseSchema
from apiflask import HTTPError
from app.blueprints.rentals.service import RentalsService

@rental_bp.route('/')
def index():
    return 'This is the user Blueprint'

@rental_bp.get('/view_rentals')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsResponseSchema(many = True))
def view_rentals():
    success, response = RentalsService.view_rentals()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)