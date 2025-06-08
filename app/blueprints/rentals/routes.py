from flask import request, redirect, url_for, flash, current_app, render_template, session
from apiflask import HTTPError
from app.models.rentals import Rentals
from app.blueprints.rentals import rental_bp
from app.blueprints.rentals.service import RentalsService
from app.blueprints.rentals.schemas import RentalsSchema, RentalRequestSchema
from app.models.users import Users
from app.models.cars import Cars
from app.extensions import auth
from app.blueprints import role_required
from app.extensions import db
from datetime import datetime, timedelta
from authlib.jose import jwt

# @rental_bp.route('/')
# def index():
#     return 'This is the rentals Blueprint'

# --- View rentals
@rental_bp.route('/list_rentals')
def view_rentals():
    token = request.cookies.get('access_token')
    if not token:
        flash("Looks like you're not signed in. Sign in first!", "warning")
        return redirect(url_for('main.login'))
    try:
        public_key = current_app.config['PUBLIC_KEY']
        claims = jwt.decode(token, public_key)
        claims.validate()
    except Exception as ex:
        flash("Looks like you're not signed in. Sign in first!", "danger")
        return redirect(url_for('main.logout'))
    
    user_roles = claims.get("roles", [])
    role_names = [role_dict.get('role_name') for role_dict in user_roles if role_dict.get('role_name')]

    if "Administrator" in role_names or "Clerk" in role_names:
        success, rentals = RentalsService.view_rentals()
        is_admin = True if "Administrator" in role_names else False
        is_clerk = True if "Clerk" in role_names else False
    else:
        success, rentals = RentalsService.view_rentals()

    if not success:
        flash(rentals, "danger")
        rentals = []
    return render_template('rentals.html', rentals=rentals, is_admin=is_admin, is_clerk=is_clerk)

# @rental_bp.route('/list_rentals')
# def view_rentals():
#     # Check if user is logged in and is admin/clerk
#     if not session.get("user") or session.get("role") not in ("Administrator", "Clerk"):
#         flash("Unauthorized", "danger")
#         return redirect(url_for('main.login'))

#     success, rentals = RentalsService.view_rentals()
#     if not success:
#         flash(rentals, "danger")
#         rentals = []

#     return render_template('rentals.html', rentals=rentals)

# --- View rentals for a user
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
@rental_bp.route('/rent/<int:cid>', methods=["POST"])
def rent_car_form(cid):
    try:
        token = request.cookies.get('access_token')
        if not token:
            flash("Looks like you're not signed in. Sign in first!", "warning")
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
            flash("Rental request submitted!", "info")
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
@rental_bp.post('/api/approve/<int:rentalid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def approve_rental(rentalid):
    # renterid = json_data.get("renterid")
    success, response = RentalsService.approve_rental(rentalid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@rental_bp.route('/approve/<int:rentalid>', methods=["POST"])
@rental_bp.doc(tags=["rentals"])
def approve_rental_form(rentalid):
    try:
        token = request.cookies.get('access_token')
        if not token:
            flash("Looks like you're not signed in. Sign in first!", "warning")
            return redirect(url_for('main.login'))
        try:
            public_key = current_app.config['PUBLIC_KEY']
            claims = jwt.decode(token, public_key)
            claims.validate()
        except Exception as ex:
            flash("Unauthorized: Invalid token!", "danger")
            return redirect(url_for('main.rentals.view_rentals'))
    except Exception as ex:
        flash(f"Error processing rental: {ex}", "danger")
        return redirect(url_for('main.rentals.view_rentals'))
    success, response = RentalsService.approve_rental(rentalid)
    if success:
        flash("Rental approved!", "success")
        return redirect(url_for('main.rentals.view_rentals'))

# --- Stop a rental
@rental_bp.post('/stop/<int:rentalid>')
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def stop_rental(rentalid):
    try:
        success, response = RentalsService.set_car_rentstatus(rentalid, {"rentstatus": "Available"})
        if success:
            return response, 200
        raise HTTPError(message=response, status_code=400)
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400
