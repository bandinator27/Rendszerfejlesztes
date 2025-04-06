from app.blueprints.cars import car_bp
from app.blueprints.cars.schemas import CarsResponseSchema
from apiflask import HTTPError
from app.blueprints.cars.service import CarsService

@car_bp.route('/')
def index():
    return 'This is the cars Blueprint'

@car_bp.get('/view_cars')
@car_bp.doc(tags=["cars"])
@car_bp.output(CarsResponseSchema(many = True))
def view_cars():
    success, response = CarsService.view_cars()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)