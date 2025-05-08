from app.blueprints.rentals import rental_bp
from app.blueprints.rentals.schemas import RentalsSchema
from apiflask import HTTPError
from app.blueprints.rentals.service import RentalsService
from app.database import auth
from app.blueprints import role_required

@rental_bp.route('/')
def index():
    return 'This is the user Blueprint'

@rental_bp.get('/view_rentals')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema(many = True))
def view_rentals():
    success, response = RentalsService.view_rentals()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@rental_bp.get('/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalsSchema, location="json")
@rental_bp.auth_required(auth)
@role_required(["User"])
def rent_car(cid, json_data):
    success, response = RentalsService.rent_car(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@rental_bp.post('/rentstatus/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalsSchema, location="json")
@rental_bp.auth_required(auth)
#@role_required(["User"])
def set_car_rentstatus(cid, json_data):
    success, response = RentalsService.set_car_rentstatus(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
