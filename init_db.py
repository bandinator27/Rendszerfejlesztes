from app import create_app
from config import Config
from app.extensions import db
from app.models.cars import Cars
from app.models.rentals import Rentals
from app.models.roles import Roles
from app.models.users import Users
from app.models.addresses import Addresses
from werkzeug.security import generate_password_hash
from datetime import datetime

app = create_app(config_class=Config)
app.app_context().push()
db.drop_all()  # Előző adatbázis törlése, ha van
db.create_all()

# --- ADDRESSES test data
db.session.add_all([
        Addresses(city="Veszprém", street="Teszt utca 1", postalcode=8200),
        Addresses(city="Veszprém", street="Teszt utca 2", postalcode=8200)
    ])

# --- ROLES test data
db.session.add_all([
        Roles(role_name="User"),
        Roles(role_name="Clerk"),
        Roles(role_name="Administrator")
    ])

# --- USERS test data
db.session.add_all([
        Users(
            username="bela",
            password=generate_password_hash("teszt123"),
            password_salt="salty",
            address_id=1,
            email="tesztbela@berauto.hu",
            phone_number="+3670123456",
        ),
        Users(
            username="jani",
            password=generate_password_hash("teszt123"),
            password_salt="salty",
            address_id=2,
            email="tesztjani@berauto.hu",
            phone_number="+3670123457",
        ),
        Users(
            username="admin",
            password=generate_password_hash("admin123"),
            password_salt="salty",
            address_id=1,
            email="admin@berauto.hu",
            phone_number="+36301234567",
        )])
# role assignments
bela = db.session.get(Users, 1)
bela.roles.append(db.session.get(Roles, 1))  # TesztBela User

jani = db.session.get(Users, 2)
jani.roles.append(db.session.get(Roles, 1))  # TesztJani User
jani.roles.append(db.session.get(Roles, 2))  # TesztJani Clerk

admin = db.session.get(Users, 3)
admin.roles.append(db.session.get(Roles, 1))  # admin Administrator
admin.roles.append(db.session.get(Roles, 3))

# --- CARS test data
db.session.add_all([
    Cars(numberplate="CRT-135", rentable=1, price=45, year = 2008, manufacturer="Citroen", model="C3", color="Silver", seats=5, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=73, kmcount=531156, enginetype="1.4 SX", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="HYU-359", rentable=1, price=10, year = 2007, manufacturer="Hyundai", model="Accent", color="Metallic Green", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=88, kmcount=375987, enginetype="1.5 GLS", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="TYC-335", rentable=1, price=55, year = 2015, manufacturer="Toyota", model="Yaris Cross", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=125, kmcount=231156, enginetype="1.5 VVT-i", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="ERT-126", rentable=1, price=39, year = 2006, manufacturer="Alfa Romeo", model="Giulietta", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=220, power=105, kmcount=267156, enginetype="1.6 JTDM", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="RIX-335", rentable=1, price=25, year = 2015, manufacturer="Hyundai", model="i10", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=87, kmcount=231156, enginetype="1.25 MPi", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="HYU-126", rentable=1, price=19, year = 2006, manufacturer="Hyundai", model="Accent", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=88, kmcount=267156, enginetype="1.5 GLS", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="RIX-126", rentable=1, price=19, year = 2016, manufacturer="Hyundai", model="i10", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=87, kmcount=267156, enginetype="1.25 MPi", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="HYU-135", rentable=1, price=15, year = 2008, manufacturer="Hyundai", model="Accent", color="Silver", seats=5, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=180, power=81, kmcount=531156, enginetype="1.5 CRDi", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="RIX-957", rentable=1, price=17, year = 2012, manufacturer="Hyundai", model="i10", color="Yellow", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=87, kmcount=441345, enginetype="1.25 MPi", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="CRT-757", rentable=1, price=37, year = 2022, manufacturer="Citroen", model="C3", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=73, kmcount=411345, enginetype="1.4 SX", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="RIX-359", rentable=1, price=10, year = 2017, manufacturer="Hyundai", model="i10", color="Metallic Green", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=87, kmcount=375987, enginetype="1.25 MPi", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="CRT-359", rentable=1, price=30, year = 2007, manufacturer="Citroen", model="C3", color="Metallic Green", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Electric", topspeed=240, power=113, kmcount=375987, enginetype="e-C3", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="TYC-518", rentable=1, price=45, year = 2018, manufacturer="Toyota", model="Yaris Cross", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=230, power=125, kmcount=162148, enginetype="1.5 VVT-i", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="HYU-335", rentable=1, price=25, year = 2005, manufacturer="Hyundai", model="Accent", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=88, kmcount=231156, enginetype="1.5 GLS", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="CRT-426", rentable=1, price=39, year = 2020, manufacturer="Citroen", model="C3", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=73, kmcount=67156, enginetype="1.4 SX", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="RIX-518", rentable=1, price=15, year = 2018, manufacturer="Hyundai", model="i10", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=210, power=87, kmcount=162148, enginetype="1.25 MPi", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="HYU-518", rentable=1, price=15, year = 2008, manufacturer="Hyundai", model="Accent", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=210, power=88, kmcount=162148, enginetype="1.5 GLS", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="TYC-126", rentable=1, price=49, year = 2016, manufacturer="Toyota", model="Yaris Cross", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=125, kmcount=267156, enginetype="1.5 VVT-i", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="RIX-426", rentable=1, price=19, year = 2010, manufacturer="Hyundai", model="i10", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=67, kmcount=67156, enginetype="1.0i", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="RIX-135", rentable=1, price=15, year = 2018, manufacturer="Hyundai", model="i10", color="Silver", seats=5, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=67, kmcount=531156, enginetype="1.0i", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="HYU-957", rentable=1, price=17, year = 2002, manufacturer="Hyundai", model="Accent", color="Yellow", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=210, power=88, kmcount=441345, enginetype="1.5 GLS", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="ERT-757", rentable=1, price=37, year = 2022, manufacturer="Alfa Romeo", model="Giulietta", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=220, power=105, kmcount=411345, enginetype="1.4 TB", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TYC-957", rentable=1, price=47, year = 2012, manufacturer="Toyota", model="Yaris Cross", color="Yellow", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=125, kmcount=441345, enginetype="1.5 VVT-i", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="RIX-818", rentable=1, price=15, year = 2015, manufacturer="Hyundai", model="i10", color="White", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=180, power=67, kmcount=162348, enginetype="1.0i", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="RIX-757", rentable=1, price=17, year = 2012, manufacturer="Hyundai", model="i10", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=67, kmcount=411345, enginetype="1.0i", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="ERT-359", rentable=1, price=30, year = 2007, manufacturer="Alfa Romeo", model="Giulietta", color="Metallic Blue", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=220, power=105, kmcount=375987, enginetype="1.6 JTDM", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TYC-359", rentable=1, price=40, year = 2017, manufacturer="Toyota", model="Yaris Cross", color="Metallic Green", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=125, kmcount=375987, enginetype="1.5 VVT-i", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="CRT-957", rentable=1, price=37, year = 2012, manufacturer="Citroen", model="C3", color="Yellow", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Electric", topspeed=240, power=113, kmcount=441345, enginetype="e-C3", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="RIX-959", rentable=1, price=10, year = 2017, manufacturer="Hyundai", model="i10", color="Metallic Blue", seats=2, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=67, kmcount=475987, enginetype="1.0i", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="hyundaii10.jpg"),
    Cars(numberplate="CRT-335", rentable=1, price=45, year = 2005, manufacturer="Citroen", model="C3", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Electric", topspeed=240, power=113, kmcount=231156, enginetype="e-C3", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="TOY-335", rentable=1, price=35, year = 2015, manufacturer="Toyota", model="Yaris", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=111, kmcount=231156, enginetype="1.5 Dual VVT-iE", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="TYC-135", rentable=1, price=45, year = 2018, manufacturer="Toyota", model="Yaris Cross", color="Silver", seats=5, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Hybrid", topspeed=210, power=92, kmcount=31156, enginetype="1.5 Hybrid", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="HYU-757", rentable=1, price=17, year = 2002, manufacturer="Hyundai", model="Accent", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=180, power=81, kmcount=411345, enginetype="1.5 CRDi", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="CRT-126", rentable=1, price=39, year = 2006, manufacturer="Citroen", model="C3", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Electric", topspeed=240, power=113, kmcount=267156, enginetype="e-C3", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="CRT-518", rentable=1, price=35, year = 2018, manufacturer="Citroen", model="C3", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Electric", topspeed=240, power=113, kmcount=162148, enginetype="e-C3", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="TOY-957", rentable=1, price=37, year = 2012, manufacturer="Toyota", model="Yaris", color="Yellow", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=111, kmcount=441345, enginetype="1.5 Dual VVT-iE", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="CRT-818", rentable=1, price=35, year = 2015, manufacturer="Citroen", model="C3", color="White", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=180, power=73, kmcount=162348, enginetype="1.4 SX", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="TOY-135", rentable=1, price=35, year = 2018, manufacturer="Toyota", model="Yaris", color="Silver", seats=5, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=210, power=90, kmcount=531156, enginetype="1.4 D-4D", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="HYU-426", rentable=1, price=19, year = 2000, manufacturer="Hyundai", model="Accent", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=180, power=81, kmcount=67156, enginetype="1.5 CRDi", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="CRT-959", rentable=1, price=30, year = 2017, manufacturer="Citroen", model="C3", color="Metallic Blue", seats=2, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=180, power=73, kmcount=475987, enginetype="1.4 SX", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="citroenc3.jpg"),
    Cars(numberplate="ERT-959", rentable=1, price=30, year = 2017, manufacturer="Alfa Romeo", model="Giulietta", color="Metallic Blue", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=220, power=105, kmcount=475987, enginetype="1.4 TB", extras="AC, , ESP, MSR, ASR, electric steering, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TOY-126", rentable=1, price=39, year = 2016, manufacturer="Toyota", model="Yaris", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=111, kmcount=267156, enginetype="1.5 Dual VVT-iE", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="TOY-359", rentable=1, price=30, year = 2017, manufacturer="Toyota", model="Yaris", color="Metallic Green", seats=4, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=230, power=111, kmcount=375987, enginetype="1.5 Dual VVT-iE", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="ERT-818", rentable=1, price=35, year = 2015, manufacturer="Alfa Romeo", model="Giulietta", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=220, power=105, kmcount=162348, enginetype="1.4 TB", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="HYU-959", rentable=1, price=10, year = 2007, manufacturer="Hyundai", model="Accent", color="Metallic Blue", seats=2, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=180, power=81, kmcount=475987, enginetype="1.5 CRDi", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="TOY-518", rentable=1, price=35, year = 2018, manufacturer="Toyota", model="Yaris", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Petrol", topspeed=230, power=111, kmcount=162148, enginetype="1.5 Dual VVT-iE", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="TYC-426", rentable=1, price=49, year = 2010, manufacturer="Toyota", model="Yaris Cross", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Hybrid", topspeed=210, power=92, kmcount=7156, enginetype="1.5 Hybrid", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="TOY-757", rentable=1, price=37, year = 2012, manufacturer="Toyota", model="Yaris", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=210, power=90, kmcount=411345, enginetype="1.4 D-4D", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="ERT-335", rentable=1, price=45, year = 2005, manufacturer="Alfa Romeo", model="Giulietta", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=220, power=105, kmcount=231156, enginetype="1.6 JTDM", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TYC-757", rentable=1, price=47, year = 2012, manufacturer="Toyota", model="Yaris Cross", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Hybrid", topspeed=210, power=92, kmcount=11345, enginetype="1.5 Hybrid", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="ERT-518", rentable=1, price=35, year = 2018, manufacturer="Alfa Romeo", model="Giulietta", color="Red", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Diesel", topspeed=220, power=105, kmcount=162148, enginetype="1.6 JTDM", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TOY-818", rentable=1, price=35, year = 2015, manufacturer="Toyota", model="Yaris", color="White", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Diesel", topspeed=210, power=90, kmcount=162348, enginetype="1.4 D-4D", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="HYU-818", rentable=1, price=15, year = 2005, manufacturer="Hyundai", model="Accent", color="White", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Diesel", topspeed=180, power=81, kmcount=162348, enginetype="1.5 CRDi", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="hyundaiaccent.jpg"),
    Cars(numberplate="TYC-818", rentable=1, price=45, year = 2015, manufacturer="Toyota", model="Yaris Cross", color="White", seats=4, interior="Carbon", bodytype="Hatchback", gearbox="automatic", doors=4, fueltype="Hybrid", topspeed=210, power=92, kmcount=62348, enginetype="1.5 Hybrid", extras="heated seats, AC, tempomat, ESP, MSR, ASR, start-stop, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="TOY-426", rentable=1, price=39, year = 2010, manufacturer="Toyota", model="Yaris", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=210, power=90, kmcount=67156, enginetype="1.4 D-4D", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="ERT-135", rentable=1, price=45, year = 2008, manufacturer="Alfa Romeo", model="Giulietta", color="Silver", seats=4, interior="Dark textile", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Petrol", topspeed=220, power=105, kmcount=531156, enginetype="1.4 TB", extras="heated seats, AC, tempomat, ESP, MSR, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TOY-959", rentable=1, price=30, year = 2017, manufacturer="Toyota", model="Yaris", color="Metallic Blue", seats=2, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Diesel", topspeed=210, power=90, kmcount=475987, enginetype="1.4 D-4D", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="toyotayaris.jpg"),
    Cars(numberplate="ERT-426", rentable=1, price=39, year = 2020, manufacturer="Alfa Romeo", model="Giulietta", color="Black", seats=4, interior="Leather", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Petrol", topspeed=220, power=105, kmcount=67156, enginetype="1.4 TB", extras="heated seats, AC, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg"),
    Cars(numberplate="TYC-959", rentable=1, price=40, year = 2017, manufacturer="Toyota", model="Yaris Cross", color="Metallic Blue", seats=2, interior="Dark textile", bodytype="Sedan", gearbox="manual", doors=4, fueltype="Hybrid", topspeed=210, power=92, kmcount=75987, enginetype="1.5 Hybrid", extras="AC, ESP, MSR, ASR, electric steering, central-lock", image_url="toyotayariscross.jpg"),
    Cars(numberplate="ERT-957", rentable=1, price=37, year = 2012, manufacturer="Alfa Romeo", model="Giulietta", color="Gold", seats=4, interior="Leather and wood", bodytype="Hatchback", gearbox="manual", doors=4, fueltype="Diesel", topspeed=220, power=105, kmcount=441345, enginetype="1.6 JTDM", extras="AC, tempomat, ESP, ASR, electric steering, start-stop, central-lock", image_url="alfaromeogiulietta.jpg")
    ])

# --- RENTALS test data
db.session.add_all([
        Rentals(
            carid=1,
            renterid=1,
            rentstart=datetime.strptime("2025-06-07", "%Y-%m-%d"),
            rentstatus="Rented",
            rentduration=1,
            rentprice=500,
            renteraddress="Veszprém, Privát utca 1",
            renterphonenum="+36201234567"
        ),
        Rentals(
            carid=2,
            renterid=3,
            rentstart=datetime.strptime("2025-06-07", "%Y-%m-%d"),
            rentstatus="Rented",
            rentduration=1,
            rentprice=500,
            renteraddress="Veszprém, Privát utca 1",
            renterphonenum="+36201234567"
        ),
        Rentals(
            carid=3,
            renterid=2,
            rentstart=datetime.strptime("2025-05-18", "%Y-%m-%d"),
            rentstatus="Pending",
            rentduration=15,
            rentprice=1500,
            renteraddress="Veszprém, Privát utca 2",
            renterphonenum="+36701234568"
        )])

db.session.commit()