from app.database import db
from app.blueprints.rentals.schemas import RentalsSchema
from app.models.rentals import Rentals

from sqlalchemy import select

class RentalsService:

    @staticmethod
    def view_rentals():
        try:
            rental = db.session.query(Rentals).all()
            
        except Exception as ex:
            return False, "Váratlan hiba történt!"
        return True, RentalsSchema().dump(rental, many = True)
    
    @staticmethod
    def rent_car(carid, request):
        try:
            rental = db.session.execute(select(Rentals).filter(Rentals.carid == carid, Rentals.rentstatus == "Rented")).scalar_one_or_none()
            if rental:
                return False, "Ez az autó foglalt"
            
            rent = Rentals(
                    request["carid"],
                    request["renterid"],
                    request["rentedat"],
                    request["rentstatus"],
                    request["rentduration"],
                    request["rentprice"],
                    request["renteraddress"],
                    request["renterphonenum"]
            )
            db.session.add(rent)
            db.session.commit()
            
        except Exception as ex:
            return False, "Váratlan hiba történt!"
        return True, RentalsSchema().dump(rent)
    
    @staticmethod
    def set_car_rentstatus(carid, request):
        try:
            rental = db.session.get(Rentals, carid)
            if rental is None:
                return False, "Ez a foglalás nem létezik"
        
            rental.rentstatus = request["rentstatus"]
            db.session.commit()

        except Exception as ex:
            return False, "Váratlan hiba történt!"
        return True, "Siker"