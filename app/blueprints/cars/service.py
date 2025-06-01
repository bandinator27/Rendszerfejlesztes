from app.database import db
from app.blueprints.cars.schemas import CarsSchema
from app.models.cars import Cars
from app.models.rentals import Rentals
from sqlalchemy import select

class CarsService:

# --- View all cars
    @staticmethod
    def view_cars():
        try:
            cars = db.session.query(Cars).all()
        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"
        return True, CarsSchema().dump(cars, many = True)
    
    @staticmethod
    def get_car_data(cid):
        try:
            cars = db.session.execute(select(Cars).filter(Cars.carid == cid)).scalar_one_or_none()
            if cars is None:
                return False, "No car found with this ID"
        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"
        return True, CarsSchema().dump(cars)

# --- Set car data
    @staticmethod
    def set_car_data(cid, request):
        try:
            car = db.session.get(Cars, cid)
            if car:
                car.numberplate = request["numberplate"]
                car.rentable = request["rentable"]
                car.price = request["price"]
                car.manufacturer = request["manufacturer"]
                car.model = request["model"]
                car.color = request["color"]
                car.seats = request["seats"]
                car.interior = request["interior"]
                car.bodytype = request["bodytype"]
                car.gearbox = request["gearbox"]
                car.doors = request["doors"]
                car.fueltype = request["fueltype"]
                car.topspeed = request["topspeed"]
                car.power = request["power"]
                car.kmcount = request["kmcount"]
                car.enginetype = request["enginetype"]
                car.extras = request["extras"]
                db.session.commit()
                return True, "Car added to database!"
                    
        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"

# --- Add a new car
    @staticmethod
    def add_car(request):
        try:
            car = Cars(**request)
            db.session.add(car)
            db.session.commit()
            return True, "Success! (add_car)"
        except Exception as ex:
            return False, f"Something went wrong while adding the car: {ex}"

# --- Remove a car
    @staticmethod
    def remove_car(cid):
        # 1. Check if the car exists
        car = db.session.get(Cars, cid)
        if not car:
            return False, "Car not found."

        # 2. Check if the car is currently rented or pending
        active_rental = db.session.execute(
            select(Rentals).filter(
                Rentals.carid == cid,
                Rentals.rentstatus.in_(["Rented", "Pending"])
            )).scalar_one_or_none()
        if active_rental:
            return False, "Car cannot be deleted: currently rented or pending rental."

        try:
            db.session.delete(car) # 3. Delete the car
            db.session.commit()
            return True, f"Car with ID:{cid} has been deleted."
        except Exception as ex:
            db.session.rollback()
            return False, f"Database error: {ex}"

