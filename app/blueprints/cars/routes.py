from app.blueprints.cars import car_bp
from app.blueprints.cars.schemas import CarsSchema, CarsFilterSchema
from apiflask import HTTPError
from app.blueprints.cars.service import CarsService
from app.extensions import auth, db
from app.blueprints import role_required
from app.models.cars import Cars
from sqlalchemy import select, func
import os, uuid
from werkzeug.utils import secure_filename
from flask import request, redirect, url_for, flash, current_app, render_template
from authlib.jose import jwt

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

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@car_bp.route('/add', methods=["POST"])
def add_car_form():
    form_data = request.form.to_dict()
    form_data['rentable'] = 1
    token = request.cookies.get('access_token')
    if not token:
        flash("Looks like you're not signed in. Sign in first!", "danger")
        return redirect(url_for('main.login'))
    try:
        public_key = current_app.config['PUBLIC_KEY']
        claims = jwt.decode(token, public_key)
        claims.validate()
    except Exception as ex:
        flash("Unauthorized: invalid token. Sign in again!", "danger")
        return redirect(url_for('main.logout'))

    user_roles = [r['role_name'] for r in claims.get('roles', [])]
    if "Administrator" not in user_roles:
        flash("You don't have permission to add a car!", "warning")
        return redirect(url_for('main.home'))
    
    new_numberplate = form_data.get('numberplate')
    if not new_numberplate:
        flash("A numberplate is required to add a car.", "danger")
        return render_template("admin.html")

    # Query the database for existing cars with the same numberplate (case-insensitive)
    existing_car = db.session.execute(
        select(Cars).filter(func.lower(Cars.numberplate) == func.lower(new_numberplate))
    ).scalar_one_or_none()

    if existing_car:
        flash(f"A car with the numberplate '{new_numberplate}' already exists. Numberplates must be unique.", "warning")
        return render_template("admin.html")

    file = request.files['car_image']
    if file.filename == '':
        flash("Select an image!", "warning")
        return render_template("admin.html")

    # Validate the file type and save it
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = str(uuid.uuid4().hex) + '.' + file_extension
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        try:
            file.save(filepath)
            form_data['image_url'] = unique_filename
        except Exception as e:
            flash(f"Error saving image: {e}", "danger")
            return render_template("admin.html")
    else:
        flash("Invalid image file type. Only PNG, JPG, JPEG is allowed.", "warning")
        return render_template("admin.html")

    success, response = CarsService.add_car(form_data)
    if success:
        flash("Car added successfully!", "success")
        return redirect(url_for('main.admin_page'))
    
    flash("Failed to add car!", "danger")
    return redirect(url_for('main.admin_page'))

@car_bp.route('/edit/<int:cid>', methods=["POST"])
@car_bp.doc(tags=["car"])
def edit_car_form(cid):
    form_data = request.form.to_dict()
    #form_data['rentable'] = 1
    token = request.cookies.get('access_token')
    if not token:
        flash("Looks like you're not signed in. Sign in first!", "danger")
        return redirect(url_for('main.login'))
    try:
        public_key = current_app.config['PUBLIC_KEY']
        claims = jwt.decode(token, public_key)
        claims.validate()
    except Exception as ex:
        flash("Unauthorized: invalid token. Sign in again!", "danger")
        return redirect(url_for('main.logout'))

    user_roles = [r['role_name'] for r in claims.get('roles', [])]
    if "Administrator" not in user_roles:
        flash("You don't have permission to add a car!", "warning")
        return redirect(url_for('main.home'))

    file = request.files['car_image']
    if file.filename == '':
        flash("Select an image!", "warning")
        return redirect(url_for('main.admin_page'))

    # Validate the file type and save it
    if file and allowed_file(file.filename):
        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = str(uuid.uuid4().hex) + '.' + file_extension
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        try:
            file.save(filepath)
            form_data['image_url'] = unique_filename
        except Exception as e:
            flash(f"Error saving image: {e}", "danger")
            return redirect(url_for('main.admin_page'))
    else:
        flash("Invalid image file type. Only PNG, JPG, JPEG is allowed.", "warning")
        return redirect(url_for('main.admin_page'))

    success, response = CarsService.set_car_data(cid, form_data)
    if success:
        flash("Car edited successfully!", "success")
        return redirect(url_for('main.admin_page'))
    
    flash("Failed to add car!", "danger")
    return redirect(url_for('main.admin_page'))

# --- Delete a car
@car_bp.delete('/api/remove/<int:cid>')
@car_bp.doc(tags=["car"])
@car_bp.auth_required(auth)
@role_required(["Administrator"])
def remove_car(cid):
    success, response = CarsService.remove_car(cid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- Filter car
@car_bp.post('/filter/')
@car_bp.doc(tags=["car"])
@car_bp.input(CarsFilterSchema, location="json")
@car_bp.output(CarsSchema(many=True))
def filter_car(json_data):
    success, response = CarsService.get_car_data_filtered(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@car_bp.route('/remove/<int:cid>', methods=["POST"])
def del_car_form(cid):
    token = request.cookies.get('access_token')
    if not token:
        flash("Looks like you're not signed in. Sign in first!", "danger")
        return redirect(url_for('main.login'))
    try:
        public_key = current_app.config['PUBLIC_KEY']
        claims = jwt.decode(token, public_key)
    except Exception as ex:
        flash(f"Unauthorized: Invalid token. ({ex}). Sign in again!", "danger")
        return redirect(url_for('main.logout'))

    user_roles = [r['role_name'] for r in claims.get('roles', [])]
    if "Administrator" not in user_roles:
        flash("You don't have permission to delete a car!", "warning")
        return redirect(url_for('main.cars'))

    success, message = CarsService.remove_car(cid)

    if success:
        flash(message, "success")
        return redirect(url_for('main.cars'))
    else:
        flash(message, "danger")
        return redirect(url_for('main.cars'))