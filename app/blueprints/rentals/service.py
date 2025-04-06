from app.database import db
from app.blueprints.rentals.schemas import RentalsResponseSchema
from app.models.rentals import Rentals

from sqlalchemy import select

class RentalsService:

    @staticmethod
    def view_rentals(request):
        try:
            rental = db.session.execute(select(Rentals).filter_by(carid=1)).scalars()
            
        except Exception as ex:
            return False, "Incorrect rental data!"
        return True, RentalsResponseSchema().dump(rental, many = True)