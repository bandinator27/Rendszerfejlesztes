from app.blueprints.rentals import rental_bp
from app.blueprints import main_bp
from app.blueprints.rentals.schemas import RentalsSchema, RentalRequestSchema
from apiflask import HTTPError
from app.blueprints.rentals.service import RentalsService
from app.extensions import auth
from app.blueprints import role_required
from app.models.users import Users
from app.extensions import db

# @rental_bp.route('/')
# def index():
#     return 'This is the rentals Blueprint'

# --- View rentals
@rental_bp.get('/view_rentals')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema(many = True))
def view_rentals():
    success, response = RentalsService.view_rentals()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@rental_bp.get('/view_rentals_user')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema(many = True))
@rental_bp.auth_required(auth)
def view_rentals_user():
    success, response = RentalsService.view_rentals_user(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Renting
from flask import request, redirect, url_for, flash, current_app
from app.extensions import db
from app.models.rentals import Rentals
from app.models.cars import Cars
from datetime import datetime, timedelta
from authlib.jose import jwt

@rental_bp.route('/rent/<int:cid>', methods=["POST"])
def rent_car_form(cid):
    try:
        token = request.cookies.get('access_token')
        if not token:
            flash("Unauthorized: No token!", "danger")
            return redirect(url_for('main.login'))

        try:
            public_key = current_app.config['PUBLIC_KEY']
            claims = jwt.decode(token, public_key)
            claims.validate()
        except Exception as ex:
            flash("Unauthorized: Invalid token!", "danger")
            return redirect(url_for('main.login'))

        data = request.form.to_dict()
        rentstart = data.get("rentstart")
        try:
            rentduration = int(data.get("rentduration", "0"))
        except ValueError:
            flash("Rental duration must be a number.", "warning")
            return redirect(url_for('main.cars'))

        if not rentstart or not rentduration:
            flash("Missing rental start date or duration.", "warning")
            return redirect(url_for('main.cars'))

        # Print for debugging
        print(f"Received rentstart: {rentstart}")
        
        try:
            rent_start_dt = datetime.strptime(rentstart, "%Y-%m-%d")
            if rent_start_dt.date() < datetime.now().date():
                flash("Rental start date cannot be in the past.", "warning")
                return redirect(url_for('main.cars'))
        except ValueError as ve:
            print(f"Date parsing error: {ve}")
            flash("Invalid date format. Please use the date picker.", "warning")
            return redirect(url_for('main.cars'))

        if rentduration <= 0:
            flash("Rental duration must be at least 1 day.", "warning")
            return redirect(url_for('main.cars'))

        user_id = claims.get('user_id')
        user = db.session.get(Users, user_id)
        if not user:
            flash("User not found.", "danger")
            return redirect(url_for('main.login'))

        rent_end_dt = rent_start_dt + timedelta(days=int(rentduration))

        active_rentals = db.session.query(Rentals).filter(
            Rentals.carid == cid,
            Rentals.rentstatus.in_(["Rented", "Pending"])).all()

        for rental in active_rentals:
            existing_start = rental.rentstart
            rental_duration = int(rental.rentduration)
            existing_end = existing_start + timedelta(days=rental_duration)
            if (rent_start_dt <= existing_end and rent_end_dt >= existing_start):
                flash(f"Car #{cid} is already rented during that time.", "warning")
                return redirect(url_for('main.cars'))

        car = db.session.get(Cars, cid)
        if not car:
            flash(f"Car #{cid} not found.", "danger")
            return redirect(url_for('main.cars'))

        rental_data = {
            "carid": cid,
            "renterid": user.id,
            "rentstart": rent_start_dt,
            "rentduration": int(rentduration),
            "rentprice": car.price * rentduration,
            "renteraddress": f"{user.address.postalcode} {user.address.city}, {user.address.street}",
            "renterphonenum": user.phone_number,
            "rentstatus": "Pending"
        }
        
        print(f"Rental data being sent to service: {rental_data}")
        print(f"rentduration type: {type(rental_data['rentduration'])}")

        success, response = RentalsService.rent_car(cid, rental_data)
        if success:
            flash("Rental request submitted!", "success")
        else:
            flash(response, "danger")
        return redirect(url_for('main.cars'))

    except Exception as ex:
        flash(f"Error processing rental: {ex}", "danger")
        return redirect(url_for('main.cars'))


@rental_bp.post('api/rent/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalRequestSchema, location="json")
@rental_bp.auth_required(auth)
def rent_car(cid, json_data):
    try:
        # Get user ID from the JWT token, other details from the database
        user_id = auth.current_user.get("user_id")
        user = db.session.get(Users, user_id)
        if not user:
            raise HTTPError(message="User not found", status_code=404)

        rental_data = {
            "carid": cid,
            "renterid": user_id,
            "rentstart": json_data["rentstart"],
            "rentduration": json_data["rentduration"],
            "rentprice": json_data["rentprice"],
            "renteraddress": f"{user.address.postalcode} {user.address.city}, {user.address.street}",
            "renterphonenum": user.phone_number,
            "rentstatus": "Pending"
        }
        success, response = RentalsService.rent_car(cid, rental_data)
        if success:
            return response, 200
        return {"message": response}, 400
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400

@rental_bp.post('/rentstatus/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalsSchema, location="json")
@rental_bp.auth_required(auth)
#@role_required(["User"])
def set_car_rentstatus(cid, json_data):
    success, response = RentalsService.set_car_rentstatus(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Approving a rental
@rental_bp.post('/approve/<int:carid>/<int:renterid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def approve_rental(carid, renterid):
    # renterid = json_data.get("renterid")
    success, response = RentalsService.approve_rental(carid, renterid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Stop a rental
@rental_bp.post('/stop/<int:carid>/<int:renterid>')
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def stop_rental(carid, renterid):
    try:
        success, response = RentalsService.set_car_rentstatus(carid, {"renterid": renterid, "rentstatus": "Available"})
        if success:
            return response, 200
        raise HTTPError(message=response, status_code=400)
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400
