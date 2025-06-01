from app.database import db
from app.blueprints.rentals.schemas import RentalsSchema
from app.models.rentals import Rentals
from sqlalchemy import select
from datetime import datetime

class RentalsService:
    @staticmethod
    def view_rentals():
        try:
            rental = db.session.query(Rentals).all()
        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, RentalsSchema().dump(rental, many=True)

# --- RENTING
    @staticmethod
    def rent_car(carid, request):
        try:
            # Validate required fields
            required_fields = [
                "carid",
                "renterid",
                "rentstart",
                "rentduration",
                "rentprice",
            ]
            for field in required_fields:
                if field not in request:
                    return False, f"Missing required field: {field}"
            try:
                request["rentstart"] = datetime.strptime(request["rentstart"], "%Y-%m-%d")
            except ValueError:
                return False, "Invalid date format. Use YYYY-MM-DD (Optional: HH:MM:SS)"

            # Check if current user already has a rental for this car
            existing_rental = db.session.get(Rentals, (carid, request["renterid"]))
            if existing_rental:
                return False, f"You already have a rental for Car #{carid}."

            # Check if car is already rented/pending
            active_rental = db.session.execute(
                select(Rentals).filter(
                    Rentals.carid == carid,
                    Rentals.rentstatus.in_(["Rented", "Pending"]),
                )).scalar_one_or_none()

            if active_rental:
                return False, f"Car #{carid} is currently unavailable."

            # Otherwise create new rental
            rent = Rentals(**request)
            db.session.add(rent)
            db.session.commit()

            return True, RentalsSchema().dump(rent)

        except Exception as ex:
            db.session.rollback() # Rollback in case of error
            return False, f"Database error (rent_car service). Details: {ex}"

# --- APPROVE RENTAL
    @staticmethod
    def approve_rental(carid, renterid):
        try:
            rental = db.session.execute(
                select(Rentals).filter_by(
                    carid=carid,
                    renterid=renterid,
                    rentstatus="Pending"
                )).scalar_one_or_none()
            if not rental:
                return False, "No pending rental found."

            rental.rentstatus = "Rented"
            db.session.add(rental)
            db.session.commit()
            
            return True, RentalsSchema().dump(rental) # Return updated rental data
        except Exception as ex:
            db.session.rollback()
            return False, f"Error while approving rental. Details: {ex}"

# --- SET RENTAL STATUS (stop rental)
    @staticmethod
    def set_car_rentstatus(carid, request):
        try:
            renterid = request["renterid"]
            rental = db.session.get(Rentals, (carid, renterid))
            if rental is None:
                return False, "This rental does not exist."

            rental.rentstatus = request["rentstatus"]
            db.session.commit()

        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, "Rental stopped, car marked as available."