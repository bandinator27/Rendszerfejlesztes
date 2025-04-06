from app.database import db
from app.blueprints.cars.schemas import CarsResponseSchema
from app.models.cars import Cars

from sqlalchemy import select

class CarsService:

    @staticmethod
    def view_cars():
        try:
            cars = db.session.execute(select(Cars).filter_by(rentable=1)).scalars()
            
        except Exception as ex:
            return False, "Database or server error!"
        return True, CarsResponseSchema().dump(cars, many = True)