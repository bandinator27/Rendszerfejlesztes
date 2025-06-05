from app.extensions import db
from app.blueprints.rentals.schemas import RentalsSchema
from app.models.rentals import Rentals
from app.models.cars import Cars
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
            # Date should already be a datetime object from the route
            if not isinstance(request["rentstart"], datetime):
                return False, "Invalid date format received by service"

            # Validate required fields
            required_fields = ["carid", "renterid", "rentstart", "rentduration", "rentprice"]
            for field in required_fields:
                if field not in request:
                    return False, f"Missing required field: {field}"

            # Make sure rentduration is an integer
            try:
                request["rentduration"] = int(request["rentduration"])
            except (ValueError, TypeError):
                return False, "Rental duration must be a number"

            # Check if current user already has a rental for this car
            # existing_rental = db.session.get(Rentals, (carid, request["renterid"]))
            # if existing_rental:
            #     return False, f"You already have a rental for Car #{carid}."

            # Check if car is already rented/pending
            # active_rental = db.session.execute(
            #     select(Rentals).filter(
            #         Rentals.carid == carid,
            #         Rentals.rentstatus.in_(["Rented", "Pending"]),
            #     )).scalar_one_or_none()

            # if active_rental:
            #     return False, f"Car #{carid} is currently unavailable."

            # Set the car to rentable=0
            car = db.session.get(Cars, carid)
            if not car:
                return False, f"Car #{carid} not found."
            car.rentable = 0

            # Otherwise create new rental
            rental = Rentals(**request)
            db.session.add(rental)
            db.session.commit()

            return True, RentalsSchema().dump(rental)

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

# --- SET RENTAL STATUS
    @staticmethod
    def set_car_rentstatus(carid, request):
        try:
            renterid = request["renterid"]
            rental = db.session.get(Rentals, (carid, renterid))
            if rental is None:
                return False, "This rental does not exist."

            rental.rentstatus = request["rentstatus"]
            # If the rental is being marked as available, set rentable to 1
            if request["rentstatus"] in ["Available"]:
                car = db.session.get(Cars, carid)
            if car:
                car.rentable = 1
            db.session.commit()

        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, "Rental stopped, car marked as available."