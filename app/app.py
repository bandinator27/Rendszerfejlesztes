from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from datetime import datetime

app = Flask(__name__)
app.secret_key = "thisisasupersecretkey"
app.permanent_session_lifetime = timedelta(days=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()

class Users(db.Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(256))
    password_salt: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(32))
    address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(32))

class Roles(db.Model):
    __tablename__ = "Roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(32))

class Rentals(db.Model):
    __tablename__ = "Rentals"
    carid: Mapped[int] = mapped_column(primary_key = True)
    renterid: Mapped[int] = mapped_column(primary_key = True)
#    rentedat: ez majd később
    rentstatus: Mapped[str] = mapped_column(String(20))
    rentduration: Mapped[int]
    rentprice: Mapped[int]
    renteraddress: Mapped[str] = mapped_column(String(100))
    renterphonenum: Mapped[str] = mapped_column(String(32))

class Cars(db.Model):
    __tablename__ = "Cars"
    carid: Mapped[int] = mapped_column(primary_key = True)
    numberplate: Mapped[str] = mapped_column(String(32))
    rentable: Mapped[bool]
    price: Mapped[int]
    manufacturer: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(32))
    color: Mapped[str] = mapped_column(String(32))
    seats: Mapped[int]
    pictures: Mapped[str] = mapped_column(String(100))
    interior: Mapped[str] = mapped_column(String(32))
    bodytype: Mapped[str] = mapped_column(String(32))
    gearbox: Mapped[str] = mapped_column(String(32))
    doors: Mapped[int]
    fueltype: Mapped[str] = mapped_column(String(32))
    topspeed: Mapped[int]
    power: Mapped[int]
    torque: Mapped[int]
    enginetype: Mapped[str] = mapped_column(String(32))
    extras: Mapped[str] = mapped_column(String(100))

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

@app.route("/")
def home():
    if "user" in session:
        user = session["user"]
    else:
        user = "No session"
    return render_template('index.html', user=user)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        found_user = db.session.query(Users).filter_by(username=username,password=password).first()
        if found_user:
            session.permanent = True
            session["user"] = username
            flash("You have been logged in!", "info")
            return redirect(url_for("home"))
        else:
            flash("Wrong username or password!")
            return render_template('login.html')
    else:
        return render_template('login.html')

#regisztráció
@app.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        found_user = db.session.query(Users).filter_by(username=username).first()
        if found_user:
            flash("This username is taken.")
            return render_template('register.html')
        else:
            dbuser = Users(username = username, password = password,
                            password_salt = 'salty', email = 'teszt.jani@berauto.com',
                            address = 'Veszprem, privat utca 1', phone_number = '+3670123456')
            db.session.add(dbuser)
            db.session.commit()
            session.permanent = True
            session["user"] = username
            flash("You have been logged in!", "info")
            return redirect(url_for("home"))
    else:
        return render_template('register.html')

# userek kilistázása adatbázis teszteléshez
@app.route("/view/")
def view():
    return render_template('view.html', values=db.session.query(Users).all())

# session nullázás
@app.route("/logout/")
def logout():
    if "user" in session:
        session.pop("user", None)
        flash("You have been logged out!", "info")
    return redirect(url_for("login"))

@app.route("/admin/")
def admin_page():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
