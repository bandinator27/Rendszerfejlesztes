from app.extensions import db
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
    
    @staticmethod
    def get_car_data_filtered(request):
        filter_type = request['filter_type']
        filterValue = request['filterValue']

        try:
            query = Cars.query

            if filter_type:
                if filter_type == "Numberplate":
                    query = query.filter(Cars.numberplate.ilike(f'%{filterValue}%'))
                elif filter_type == "Manufacturer":
                    query = query.filter(Cars.manufacturer.ilike(f'%{filterValue}%'))
                elif filter_type == "Model":
                    query = query.filter(Cars.model.ilike(f'%{filterValue}%'))
                elif filter_type == "Color":
                    query = query.filter(Cars.color.ilike(f'%{filterValue}%'))
                elif filter_type == "Price (Maximum)":
                    try:
                        max_price = float(filterValue)
                        query = query.filter(Cars.price <= max_price)
                    except ValueError:
                        query = Cars.query.all()
                elif filter_type == "Price (Minimum)":
                    try:
                        min_price = float(filterValue)
                        query = query.filter(Cars.price >= min_price)
                    except ValueError:
                        query = Cars.query.filter(False)
                elif filter_type == "Mileage (Maximum)":
                    try:
                        max_km = int(filterValue)
                        query = query.filter(Cars.kmcount <= max_km)
                    except ValueError:
                        query = Cars.query.filter(False)
                elif filter_type == "Mileage (Minimum)":
                    try:
                        min_km = int(filterValue)
                        query = query.filter(Cars.kmcount >= min_km)
                    except ValueError:
                        query = Cars.query.filter(False)
                else:
                    pass

            if not filterValue or not filter_type:
                cars_list = Cars.query.all()
            else:
                cars_list = query.all()

        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"
        return True, CarsSchema().dump(cars_list, many=True)

# --- List available cars
    @staticmethod
    def list_available():
        try:
            cars = db.session.query(Cars).filter(Cars.rentable == 1).all()
        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"
        return True, CarsSchema().dump(cars, many=True)

# --- Set car data (modify)
    @staticmethod
    def set_car_data(cid, request):
        try:
            car = db.session.get(Cars, cid)
            if car:
                car.rentable = request["rentable"]
                car.price = request["price"]
                car.year = request["year"]
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
                car.image_url = request["image_url"]
                db.session.commit()
                return True, f"ID:{cid} car modifications saved!"
                    
        except Exception as ex:
            return False, f"Database or server error! Details: {ex}"

# --- Add a new car
    @staticmethod
    def add_car(request):
        try:
            car = Cars(**request)
            db.session.add(car)
            db.session.commit()
            return True, "Successfully added the car to the database!"
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
                Rentals.rentstatus.in_(["Rented", "Pending", "Returned"])
            )).scalars().all()
        if active_rental:
            return False, "Car cannot be deleted: currently rented, pending rental or needed for logging reasons."

        try:
            # 3. Delete the car
            db.session.delete(car)
            db.session.commit()
            return True, f"The selected car has been deleted."
        except Exception as ex:
            db.session.rollback()
            return False, f"Database error: {ex}"

