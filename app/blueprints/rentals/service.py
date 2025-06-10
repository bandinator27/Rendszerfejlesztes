from app.extensions import db
from app.blueprints.rentals.schemas import RentalsSchema
from app.models.rentals import Rentals
from app.models.cars import Cars
from app.models.users import Users
from sqlalchemy import select
from datetime import datetime

class RentalsService:

# --- VIEW RENTALS
    @staticmethod
    def view_rentals():
        try:
            rental_pending= db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Pending')).scalars().all()
            rental_rented = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Rented')).scalars().all()
            rental_returned = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Returned')).scalars().all()
            rentals = rental_pending+rental_rented+rental_returned
            #rentals = db.session.query(Rentals).all()
        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, RentalsSchema().dump(rentals, many=True)
    
    @staticmethod
    def filter_rentals(request):
        filter_type = request['filter_type']
        filterValue = request['filterValue']

        try:
            query = Rentals.query

            if filter_type:
                if filter_type == "Numberplate":
                    car = db.session.execute(select(Cars).filter(Cars.numberplate.ilike(f'%{filterValue}%'))).scalar_one_or_none()
                    query = query.filter(Rentals.carid == car.carid)
                elif filter_type == "Username":
                    user = db.session.execute(select(Users).filter(Users.username.ilike(f'%{filterValue}%'))).scalar_one_or_none()
                    query = query.filter(Rentals.renterid == user.id)
                elif filter_type == "Start date":
                    query = query.filter(Rentals.rentstart.ilike(f'%{filterValue}%'))
                elif filter_type == "Status":
                    query = query.filter(Rentals.rentstatus.ilike(f'%{filterValue}%'))
                elif filter_type == "Length (Maximum)":
                    try:
                        max_length = float(filterValue)
                        query = query.filter(Rentals.rentduration <= max_length)
                    except ValueError:
                        query = Rentals.query.all()
                elif filter_type == "Length (Minimum)":
                    try:
                        min_length = float(filterValue)
                        query = query.filter(Rentals.rentduration >= min_length)
                    except ValueError:
                        query = Rentals.query.all()
                elif filter_type == "Price (Maximum)":
                    try:
                        max_price = float(filterValue)
                        query = query.filter(Rentals.rentprice <= max_price)
                    except ValueError:
                        query = Rentals.query.all()
                elif filter_type == "Price (Minimum)":
                    try:
                        min_price = float(filterValue)
                        query = query.filter(Rentals.rentprice >= min_price)
                    except ValueError:
                        query = Rentals.query.all()
                else:
                    pass

            if not filterValue or not filter_type:
                rental_pending = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Pending')).scalars().all()
                rental_rented = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Rented')).scalars().all()
                rental_returned = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Returned')).scalars().all()
                rentals = rental_pending+rental_rented+rental_returned
            else:
                #rentals = query.all()
                rentals_pending = query.filter(Rentals.rentstatus == 'Pending').all()
                rentals_rented = query.filter(Rentals.rentstatus == 'Rented').all()
                rentals_returned = query.filter(Rentals.rentstatus == 'Returned').all()
                rentals = rentals_pending + rentals_rented + rentals_returned

        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"
        return True, RentalsSchema().dump(rentals, many=True)
    
    @staticmethod
    def view_rentals_user(user_id):
        try:
            rental_pending = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Pending', Rentals.renterid == user_id)).scalars().all()
            rental_rented = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Rented', Rentals.renterid == user_id)).scalars().all()
            rental_returned = db.session.execute(select(Rentals).filter(Rentals.rentstatus == 'Returned', Rentals.renterid == user_id)).scalars().all()
            rental = rental_pending+rental_rented+rental_returned
        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, RentalsSchema().dump(rental, many=True)
    
    @staticmethod
    def rental_get_user(user_id, cid):
        try:
            rental = db.session.execute(select(Rentals).filter(Rentals.rentalid == cid, Rentals.renterid == user_id)).scalar_one_or_none()
        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, RentalsSchema().dump(rental)
    
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
    def approve_rental(rentalid):
        try:
            rental = db.session.execute(
                select(Rentals).filter_by(
                    rentalid=rentalid,
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

# --- STOP RENTAL
    @staticmethod
    def stop_rental(rentalid):
        try:
            rental = db.session.get(Rentals, rentalid)
            if rental is None:
                return False, "This rental does not exist."

            rental.rentstatus = "Returned"

            car = db.session.get(Cars, rental.carid)
            if car:
                car.rentable = 1

            db.session.commit()

        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, "Rental stopped, car marked as available."
    
# --- DELETE RENTAL
    @staticmethod
    def delete_rental(rentalid):
        try:
            rental = db.session.get(Rentals, rentalid)
            if rental is None:
                return False, "This rental does not exist."

            rental.rentstatus = "Available"

            car = db.session.get(Cars, rental.carid)
            if car:
                car.rentable = 1
            db.session.delete(rental)
            db.session.commit()

        except Exception as ex:
            return False, f"Database error! Details: {ex}"
        return True, "Rental stopped, car marked as available."