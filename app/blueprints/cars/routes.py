from app.blueprints.cars import car_bp
from app.blueprints.cars.schemas import CarsSchema
from apiflask import HTTPError
from app.blueprints.cars.service import CarsService
from app.database import auth
from app.blueprints import role_required

@car_bp.route('/')
def index():
    return 'This is the cars Blueprint'

@car_bp.get('/view_cars')
@car_bp.doc(tags=["car"])
@car_bp.output(CarsSchema(many = True))
def view_cars():
    success, response = CarsService.view_cars()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@car_bp.get('/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.output(CarsSchema())
def get_car_data(cid):
    success, response = CarsService.get_car_data(cid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@car_bp.post('/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.input(CarsSchema, location="json")
@car_bp.auth_required(auth)
@role_required(["User"])
@role_required(["Clerk", "Administrator"])
def set_car_data(cid, json_data):
    success, response = CarsService.set_car_data(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@car_bp.post('/add')
@car_bp.doc(tags=["car"])
@car_bp.input(CarsSchema, location="json")
@car_bp.auth_required(auth)
#@role_required(["User"])
def add_car(json_data):
    success, response = CarsService.add_car(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)
