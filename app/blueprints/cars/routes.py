from app.blueprints.cars import car_bp
from app.blueprints.cars.schemas import CarsSchema
from apiflask import HTTPError
from app.blueprints.cars.service import CarsService
from app.extensions import auth
from app.blueprints import role_required

# @car_bp.route('/')
# def index():
#     return 'This is the cars Blueprint'

# --- List all cars
@car_bp.get('/view_cars')
@car_bp.doc(tags=["car"])
@car_bp.output(CarsSchema(many = True))
def view_cars():
    success, response = CarsService.view_cars()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- View one car with given id (basically search)
@car_bp.get('/view/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.output(CarsSchema())
def get_car_data(cid):
    success, response = CarsService.get_car_data(cid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- List available cars
@car_bp.get('/list_available')
@car_bp.doc(tags=["car"])
@car_bp.output(CarsSchema(many=True))
def list_available():
    success, response = CarsService.list_available()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@car_bp.post('/set/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.input(CarsSchema, location="json")
@car_bp.auth_required(auth)
@role_required(["Administrator"])
def set_car_data(cid, json_data):
    success, response = CarsService.set_car_data(cid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Add a new car
@car_bp.post('/api/add')
@car_bp.doc(tags=["car"])
@car_bp.input(CarsSchema, location="json")
@car_bp.auth_required(auth)
@role_required(["Administrator"])
def add_car(json_data):
    success, response = CarsService.add_car(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

from flask import request, render_template, redirect, url_for, flash, current_app
from authlib.jose import jwt

@car_bp.route('/add', methods=["POST"])
def add_car_form():
    form_data = request.form.to_dict()

    print(f"DEBUG: add_car_form")
    token = request.cookies.get('access_token')
    print(f"DEBUG: Token: {token}")
    if not token:
        flash("Unauthorized: No token found!", "danger")
        return redirect(url_for('main.login'))

    try:
        public_key = current_app.config['PUBLIC_KEY']
        claims = jwt.decode(token, public_key)
        claims.validate()
    except Exception as e:
        flash("Unauthorized: Invalid token!", "danger")
        return redirect(url_for('main.login'))

    user_roles = [r['role_name'] for r in claims.get('roles', [])]
    if "Administrator" not in user_roles:
        flash("Warning: You don't have access to add a car!", "warning")
        return redirect(url_for('main.home'))

    success, response = CarsService.add_car(form_data)
    if success:
        flash("Car added successfully!", "success")
        return redirect(url_for('main.home'))

    flash("Failed to add car", "danger")
    return render_template("add_car.html")

# --- Delete a car
@car_bp.delete('/remove/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.auth_required(auth)
@role_required(["Administrator"])
def remove_car(cid):
    success, response = CarsService.remove_car(cid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)