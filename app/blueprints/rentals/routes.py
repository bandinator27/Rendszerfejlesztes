from flask import request, redirect, url_for, flash, render_template, session
from apiflask import HTTPError
from app.models.rentals import Rentals
from app.blueprints import set_auth_headers
from app.blueprints.rentals import rental_bp
from app.blueprints.rentals.service import RentalsService
from app.blueprints.rentals.schemas import RentalsSchema, RentalRequestSchema, RentalsFilterSchema
from app.models.users import Users
from app.models.cars import Cars
from app.extensions import auth
from app.blueprints import role_required
from app.extensions import db
from datetime import datetime, timedelta
import requests

# --- View rentals
@rental_bp.get('/api/view_rentals')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema(many = True))
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def view_rentals_api():
    success, response = RentalsService.view_rentals()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- View rentals
@rental_bp.post('/filter')
@rental_bp.doc(tags=["rentals"])
@rental_bp.input(RentalsFilterSchema, location="json")
@rental_bp.output(RentalsSchema(many = True))
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def filter_rentals(json_data):
    success, response = RentalsService.filter_rentals(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- View rentals
@rental_bp.route('/list_rentals')
def view_rentals():

    if not session.get('user_id'):
        flash("Looks like you're not signed in. Sign in first!", "danger")
        return redirect(url_for('main.home'))

    if not ('Administrator' in session.get('role', []) or 'Clerk' in session.get('role', [])):
        flash("You don't have permission to view this!", "warning")
        return redirect(url_for('main.home'))

    cid = request.args.get('cid', type=str)
    filter_type = request.args.get('type', type=str)
    if not filter_type:
        filter_type = 'default'
    if not cid:
        cid = 'default'

    token = request.cookies.get('access_token')
    if not token:
        flash("Authentication token missing. Please log in again.", "danger")
        return redirect(url_for('main.login'))

    response = requests.post('http://localhost:5000/rental/filter',
    json={
        'filter_type': filter_type,
        'filterValue': cid
    }, headers=set_auth_headers(token))

    if response.status_code != 200:
        flash(f"Error fetching rentals: {response.text}", "danger")
        rentals = []
    else:
        rentals = response.json()

    token = request.cookies.get('access_token')
    
    numberplates = []
    for rental in rentals:
        car_data = requests.get('http://localhost:5000/car/view/'+str(rental["carid"]), headers=set_auth_headers(token))
        numberplates.append(car_data.json()['numberplate'])

    usernames = []
    for rental in rentals:
        user_data = requests.get('http://localhost:5000/user/get/'+str(rental["renterid"]), headers=set_auth_headers(token))
        usernames.append(user_data.json()['username'])

    return render_template('rentals.html', rentals=rentals, numberplates=numberplates, usernames=usernames)

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

# --- Get rental for a user
@rental_bp.get('/get/user/<int:cid>')
@rental_bp.doc(tags=["rentals"])
@rental_bp.output(RentalsSchema())
@rental_bp.auth_required(auth)
def rental_get_user(cid):
    success, response = RentalsService.rental_get_user(auth.current_user.get("user_id"), cid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Renting
@rental_bp.route('/rent/<int:cid>', methods=["POST"])
def rent_car_form(cid):
    try:
        token = request.cookies.get('access_token')
        if not token:
            flash("You have to be signed in to rent a car. Register if you don't have an account!", "warning")
            return redirect(url_for('main.login'))

        data = request.form.to_dict()
        rentstart = data.get("rentstart")
        try:
            rentduration = int(data.get("rentduration", "0"))
        except ValueError:
            flash("Rental duration must be a number.", "warning")
            return redirect(url_for('main.cars'))

        if not rentstart or not rentduration:
            flash("Please enter a date and the number of days for which you'd like to rent.", "warning")
            return redirect(url_for('main.cars'))

        try:
            rent_start_dt = datetime.strptime(rentstart, "%Y-%m-%d")
            if rent_start_dt.date() < datetime.now().date():
                flash("Time travel has not yet been invented so you have to pick a date in the present.", "warning")
                return redirect(url_for('main.cars'))
        except ValueError as ve:
            flash("Invalid date format. Please use the date picker.", "warning")
            return redirect(url_for('main.cars'))

        if rentduration <= 0:
            flash("Rental duration must be at least 1 day.", "warning")
            return redirect(url_for('main.cars'))

        if not session['user_id']:
            flash("You are not logged in!", "danger")
            return redirect(url_for('main.login'))
        
        user_id = session['user_id']
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
                flash(f"The selected car is already rented during that time.", "warning")
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
@role_required(["Clerk", "Administrator"])
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
@role_required(["Clerk", "Administrator"])
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
    success, response = RentalsService.approve_rental(rentalid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@rental_bp.route('/approve/<int:rentalid>', methods=["POST"])
@rental_bp.doc(tags=["rentals"])
def approve_rental_form(rentalid):
    if not session['user_id']:
        flash("Looks like you're not signed in. Sign in first!", "warning")
        return redirect(url_for('main.login'))
    
    token = request.cookies.get('access_token')
    response = requests.post('http://localhost:5000/rental/api/approve/'+str(rentalid), headers=set_auth_headers(token))

    #success, response = RentalsService.approve_rental(rentalid)
    if response.status_code == 200:
        flash("Rental approved!", "success")
    else:
        flash("Something went wrong!", "danger")

    return redirect(url_for('main.rentals.view_rentals'))

# --- Stop a rental
@rental_bp.post('/api/stop/<int:rentalid>')
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def stop_rental(rentalid):
    try:
        success, response = RentalsService.stop_rental(rentalid)
        if success:
            return response, 200
        raise HTTPError(message=response, status_code=400)
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400

@rental_bp.route('/stop/<int:rentalid>', methods=["POST"])
@rental_bp.doc(tags=["rentals"])
def stop_rental_form(rentalid):
    try:
        if not session['user_id']:
            flash("Looks like you're not signed in. Sign in first!", "warning")
            return redirect(url_for('main.login'))
        
        token = request.cookies.get('access_token')
        response = requests.post('http://localhost:5000/rental/api/stop/'+str(rentalid), headers=set_auth_headers(token))

        if response.status_code == 200:
            flash("The rental has ended!", "success")
        else:
            flash("Something went wrong!", "danger")

        #success, response = RentalsService.stop_rental(rentalid)
        return redirect(url_for('main.rentals.view_rentals'))
    
    except Exception as ex:
        flash(f"Error processing rental: {ex}", "danger")
        
    return redirect(url_for('main.rentals.view_rentals'))

# --- Delete a rental
@rental_bp.post('/api/delete/<int:rentalid>')
@rental_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
def delete_rental(rentalid):
    try:
        success, response = RentalsService.delete_rental(rentalid)
        if success:
            return response, 200
        raise HTTPError(message=response, status_code=400)
    except Exception as ex:
        return {"message": f"Error: {ex}"}, 400

@rental_bp.route('/delete/<int:rentalid>', methods=["POST"])
@rental_bp.doc(tags=["rentals"])
def delete_rental_form(rentalid):
    try:
        if not session['user_id']:
            flash("Looks like you're not signed in. Sign in first!", "warning")
            return redirect(url_for('main.login'))
        
        token = request.cookies.get('access_token')
        response = requests.post('http://localhost:5000/rental/api/delete/'+str(rentalid), headers=set_auth_headers(token))

        if response.status_code == 200:
            flash("The rental has been deleted!", "success")
        else:
            flash("Something went wrong!", "danger")

        #success, response = RentalsService.delete_rental(rentalid)
        return redirect(url_for('main.rentals.view_rentals'))
    
    except Exception as ex:
        flash(f"Error processing rental: {ex}", "danger")
        
    return redirect(url_for('main.rentals.view_rentals'))