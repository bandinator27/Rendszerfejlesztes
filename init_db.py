from app import create_app
from config import Config
from app.database import db
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *

app = create_app(config_class=Config)
app.app_context().push()

# előző adatbázis nullázása teszteléshez
db.session.query(Users).delete()
db.session.commit()
#teszt adatok az adatbázishoz
db.session.add_all([Users(username = 'TesztBela', password = 'teszt', password_salt = 'salty',
                        email = 'teszt.bela@berauto.com', address = 'Veszprem, privat utca 1',
                        phone_number = '+3670123456'),
                    Users(username = 'TesztJani', password = 'teszt', password_salt = 'salty',
                        email = 'teszt.jani@berauto.com', address = 'Veszprem, privat utca 2',
                        phone_number = '+3670123457')])
db.session.commit()

# előző adatbázis nullázása teszteléshez
db.session.query(Cars).delete()
db.session.commit()
#teszt adatok az adatbázishoz
db.session.add_all([Cars(numberplate = 'ERT-555', rentable = True, price = 5000,
                         manufacturer = 'Tesla', model = 'Y', color = 'Silver',
                         seats = 4, pictures = 'none', interior = 'Dark',
                        bodytype = 'Sedan', gearbox = 'automatic', doors = 4,
                         fueltype = 'Electric', topspeed = 330, power = 415,
                         torque = 1025, enginetype = 'Electric', extras = 'ABS, heated seats'),
                    Cars(numberplate = 'ABC-123', rentable = False, price = 1000,
                         manufacturer = 'Audi', model = 'A1', color = 'Black',
                         seats = 4, pictures = 'none', interior = 'Light',
                         bodytype = 'Hatchback', gearbox = 'manual', doors = 4,
                         fueltype = 'Diesel', topspeed = 270, power = 105,
                         torque = 200, enginetype = '1.9l TDI', extras = 'ABS')])
db.session.commit()