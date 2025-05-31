from app import create_app
from config import Config
from app.database import db
from app.models.cars import Cars
from app.models.rentals import Rentals
from app.models.roles import Roles
from app.models.users import Users, UserRole
from app.models.addresses import Addresses
from werkzeug.security import generate_password_hash
from sqlalchemy import delete

app = create_app(config_class=Config)
app.app_context().push()
db.drop_all()  # Előző adatbázis törlése, ha van
db.create_all()

# --- ADDRESSES teszt adatok
db.session.add_all([Addresses(city = 'Veszprém', street = 'Teszt utca 1', postalcode = 8200),
                    Addresses(city = 'Veszprém', street = 'Teszt utca 2', postalcode = 8200)
                    ])

# --- ROLES teszt adatok
db.session.add_all([Roles(role_name = 'User'),
                    Roles(role_name = 'Clerk'),
                    Roles(role_name = 'Administrator')
                    ])

# --- USERS teszt adatok
db.session.add_all([Users(username = 'TesztBela',
                          password = generate_password_hash('teszt123'),
                          password_salt = 'salty',
                          address_id = 1,
                          email = 'tesztbela@berauto.hu',
                          phone_number = '+3670123456',
                          ),
                    Users(username = 'TesztJani',
                          password = generate_password_hash('teszt123'),
                          password_salt = 'salty',
                          address_id = 2,
                          email = 'tesztjani@berauto.hu',
                          phone_number = '+3670123457',
                          ),
                    Users(username = 'admin',
                          password = generate_password_hash('admin123'),
                          password_salt = 'salty',
                          address_id = 1,
                          email = 'admin@berauto.hu',
                          phone_number = '+36301234567'
                          )
                    ])

bela = db.session.get(Users, 1)
bela.roles.append(db.session.get(Roles, 2)) # TesztBela User

jani = db.session.get(Users, 2)
jani.roles.append(db.session.get(Roles, 1)) # TesztJani User
jani.roles.append(db.session.get(Roles, 2)) # TesztJani Clerk

admin = db.session.get(Users, 3)
admin.roles.append(db.session.get(Roles,1)) # admin Administrator
admin.roles.append(db.session.get(Roles,3))

# --- CARS teszt adatok
db.session.add_all([Cars(numberplate = 'ERT-555', rentable = 1, price = 5000, manufacturer = 'Tesla', model = 'Y', 
                      color = 'Silver', seats = 4, interior = 'Dark', bodytype = 'Sedan', gearbox = 'automatic', doors = 4, fueltype = 'Electric', topspeed = 330, power = 415, torque = 1025, enginetype = 'Electric', extras = 'ABS, heated seats'),
                    Cars(numberplate = 'ABC-123', rentable = 1, price = 1000, manufacturer = 'Audi', model = 'A1', color = 'Black', seats = 4, interior = 'Light', bodytype = 'Hatchback', gearbox = 'manual', doors = 4, fueltype = 'Diesel', topspeed = 270, power = 105, torque = 200, enginetype = '1.9l TDI', extras = 'ABS'),
                    Cars(numberplate = 'DEF-456', rentable = 0, price = 4000, manufacturer = 'Skoda', model = 'Superb', color = 'Navy Blue', seats = 4, interior = 'Beige', bodytype = 'Sedan', gearbox = 'automatic', doors = 5, fueltype = 'Gasoline', topspeed = 280, power = 185, torque = 200, enginetype = '2l', extras = 'ABS, ACC')
                    ])

# --- RENTALS teszt adatok
db.session.add_all([Rentals(carid = 1,
                            renterid = 1, 
                            rentedat = "2025-06-07",
                            rentstatus = "Bérelt",
                            rentduration = 1,
                            rentprice = 500,
                            renteraddress = "Veszprém, Privát utca 1",
                            renterphonenum = "+36201234567"),
                    Rentals(carid = 2,
                            renterid = 2,
                            rentedat = "2025-05-18",
                            rentstatus = "Elérhető",
                            rentduration = 15,
                            rentprice = 1500,
                            renteraddress = "Veszprém, Privát utca 2",
                            renterphonenum = "+36701234568")
                    ])

db.session.commit()