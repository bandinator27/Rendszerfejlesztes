from app import create_app
from config import Config
from app.database import db
from app.models.cars import Cars
from app.models.rentals import Rentals
from app.models.roles import Roles
from app.models.users import Users
from app.models.addresses import Addresses
from werkzeug.security import generate_password_hash

app = create_app(config_class=Config)
app.app_context().push()
db.create_all()

# előző adatbázis nullázása teszteléshez
db.session.query(Addresses).delete()
db.session.commit()

#teszt adatok az adatbázishoz
db.session.add_all([Addresses(city = 'Veszprem', street = 'Teszt utca', postalcode = 8200),
                    Addresses(city = 'Veszprem', street = 'Teszt utca 2', postalcode = 8200)])
db.session.commit()

# előző adatbázis nullázása teszteléshez
db.session.query(Users).delete()
db.session.commit()

#teszt adatok az adatbázishoz
db.session.add_all([Users(username = 'TesztBela',
                          password = generate_password_hash('teszt123'),
                          password_salt = 'salty',
                          address_id = 1,
                          email = 'teszt.bela@berauto.com',
                          phone_number = '+3670123456'),
                    Users(username = 'TesztJani',
                          password = generate_password_hash('teszt123'),
                          password_salt = 'salty',
                          address_id = 2,
                          email = 'teszt.jani@berauto.com',
                          phone_number = '+3670123457')])
db.session.commit()

# előző adatbázis nullázása teszteléshez
db.session.query(Roles).delete()
db.session.commit()

#teszt adatok az adatbázishoz
db.session.add_all([Roles(id = 1, role_name = 'User'),
                    Roles(id = 1, role_name = 'Clerk'),
                    Roles(id = 1, role_name = 'Administrator'),
                    Roles(id = 2, role_name = 'User'),
                    Roles(id = 2, role_name = 'Clerk'),
                    Roles(id = 2, role_name = 'Administrator')])
db.session.commit()

# előző adatbázis nullázása teszteléshez
db.session.query(Cars).delete()
db.session.commit()

#teszt adatok az adatbázishoz
db.session.add_all([Cars(numberplate = 'ERT-555', rentable = 1, price = 5000,
                         manufacturer = 'Tesla', model = 'Y', color = 'Silver',
                         seats = 4, pictures = 'none', interior = 'Dark',
                        bodytype = 'Sedan', gearbox = 'automatic', doors = 4,
                         fueltype = 'Electric', topspeed = 330, power = 415,
                         torque = 1025, enginetype = 'Electric', extras = 'ABS, heated seats'),
                    Cars(numberplate = 'ABC-123', rentable = 1, price = 1000,
                         manufacturer = 'Audi', model = 'A1', color = 'Black',
                         seats = 4, pictures = 'none', interior = 'Light',
                         bodytype = 'Hatchback', gearbox = 'manual', doors = 4,
                         fueltype = 'Diesel', topspeed = 270, power = 105,
                         torque = 200, enginetype = '1.9l TDI', extras = 'ABS')])
db.session.commit()

# előző adatbázis nullázása teszteléshez
db.session.query(Rentals).delete()
db.session.commit()

#teszt adatok az adatbázishoz
db.session.add_all([Rentals(carid = 1, renterid = 1, rentstatus = "Rented",
                         rentduration = 1, rentprice = 500, renteraddress = "Veszprém, privát utca 1",
                         renterphonenum = "+36701234567"),
                    Rentals(carid = 2, renterid = 2, rentstatus = "Returned",
                         rentduration = 15, rentprice = 1500, renteraddress = "Veszprém, privát utca 2",
                         renterphonenum = "+36701234568")])
db.session.commit()