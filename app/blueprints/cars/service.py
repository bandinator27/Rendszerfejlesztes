from app.database import db
from app.blueprints.cars.schemas import CarsSchema
from app.models.cars import Cars
from sqlalchemy import select

class CarsService:

    @staticmethod
    def view_cars():
        try:
            cars = db.session.execute(select(Cars).filter(Cars.rentable == 1)).scalars()
            #cars = db.session.query(Cars).all()

        except Exception as ex:
            return False, "Database or server error!"
        return True, CarsSchema().dump(cars, many = True)
    
    @staticmethod
    def get_car_data(cid):
        try:
            cars = db.session.execute(select(Cars).filter(Cars.carid == cid)).scalar_one_or_none()
            if cars is None:
                return False, "Ezzel az ID-vel nem található autó az adatbázisban"

        except Exception as ex:
            return False, "Adatbázis vagy szerver hiba!"
        return True, CarsSchema().dump(cars)
    
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
                car.pictures = request["pictures"]
                car.interior = request["interior"]
                car.bodytype = request["bodytype"]
                car.gearbox = request["gearbox"]
                car.doors = request["doors"]
                car.fueltype = request["fueltype"]
                car.topspeed = request["topspeed"]
                car.power = request["power"]
                car.torque = request["torque"]
                car.enginetype = request["enginetype"]
                car.extras = request["extras"]
                db.session.commit()
                return True, "Success"
                    
        except Exception as ex:
            return False, "Adatbázis vagy szerver hiba!"
        
    @staticmethod
    def add_car(request):
        #try:
        car = Cars(**request)
        db.session.add(car)
        db.session.commit()
        return True, "Success"
                    
        #except Exception as ex:
        #    return False, "Something went wrong"