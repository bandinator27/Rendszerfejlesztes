from flask import current_app, redirect, url_for, render_template, request, session, flash, make_response
from app.extensions import db
from app.models.addresses import Addresses
from app.blueprints.user.schemas import PayloadSchema, RoleSchema
from app.blueprints import main_bp
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import select
from app.forms.loginform import LoginForm
from app.forms.registerform import RegisterForm

import requests
from app.blueprints import verify_token, set_auth_headers
from authlib.jose import jwt
from authlib.jose import jwt
from datetime import datetime, timedelta
@main_bp.route("/")
def home():
   if "user" in session:
       user = session["user"]
   else:
       user = "None"
   return render_template('index.html', user = user)

@main_bp.route("/login/", methods=['POST', 'GET'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login requested for user {}".format(form.username.data))
           
        login_request = requests.post('http://localhost:5000/user/login',
                        json={
                            'username': form.username.data,
                            'password': form.password.data
                        })

        login_response = login_request.json()
        if not login_response["token"]:
            flash("Wrong username or password")
            return redirect("/login")
        
        session['user'] = login_response["username"]

        data = verify_token(login_response["token"])

        role_list = []
        for role in data["roles"]:
            role_list.append(role['role_name'])

        session['role'] = role_list
        print(session['role'])
        if 'Administrator' in session['role']:
            print('Admin yaaay!')

        if 'User' in session['role']:
            print('User yaay!')

        resp = make_response(redirect(url_for('main.home')))
        resp.set_cookie('access_token', login_response["token"], httponly=True, secure=False, samesite='Lax')
            
        flash("You're signed in!", "info")
        return resp

    return render_template('login.html', name='Sign In', form=form)

    #if request.method == 'POST':
    #
    #    username = request.form.get('username')
    #    password = request.form.get('password')
    #
    #    user = db.session.query(Users).filter_by(username=username).first()
    #
    #    if user and check_password_hash(user.password, password):
    #        session['user'] = user.username
    #
    #        # Determine primary role
    #        all_roles_ordered_by_id = db.session.execute(select(Roles).order_by(Roles.id.desc())).scalars().all()
    #        role_hierarchy = [role.role_name for role in all_roles_ordered_by_id]
    #        user_role_names = [role.role_name for role in user.roles]
    #        primary_role = next((r for r in role_hierarchy if r in user_role_names), None)
    #        session['role'] = primary_role
    #
    #        payload = PayloadSchema()
    #        payload.user_id = user.id
    #        payload.roles = RoleSchema().dump(obj=user.roles, many=True)
    #        payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
    #
    #        header = {'alg': 'RS256'}
    #        claims = PayloadSchema().dump(payload)
    #        private_key = current_app.config['SECRET_KEY']
    #        token = jwt.encode(header, claims, private_key).decode()
    #
    #        resp = make_response(redirect(url_for('main.home')))
    #        resp.set_cookie('access_token', token, httponly=True, secure=False, samesite='Lax')
    #        
    #        flash("You're signed in!", "info")
    #        return resp
    #
    #    else:
    #        flash("Incorrect sign-in details!", "danger")
    #        return render_template('login.html', register=url_for('main.register'))
    #
    #return render_template('login.html', register=url_for('main.register'))

# --- Registration
@main_bp.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        register_request = requests.post('http://localhost:5000/user/register',
            json={
                'username': form.username.data,
                'password': generate_password_hash(form.username.data[::-1]+form.password.data),
                'email': form.email.data,
                'phone_number': form.phone.data,
                'address': {
                    'city': form.city.data,
                    'street': form.street.data,
                    'postalcode': form.postal.data       
                }
            })
        
        register_response = register_request.json()
        print(register_response)
        print(register_request)

        flash("Successful registration! You can now sign in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# --- List users for testing
@main_bp.route("/view/")
def view():
   return render_template('view.html', values=db.session.query(Users).all())

# --- List cars
@main_bp.route('/cars', methods=['GET'], strict_slashes=False)
def cars():
    cid = request.args.get('cid', type=str)
    filter_type = request.args.get('type', type=str)

    query = Cars.query

    if cid and filter_type:
        if filter_type == "Numberplate":
            query = query.filter(Cars.numberplate.ilike(f'%{cid}%'))
        elif filter_type == "Manufacturer":
            query = query.filter(Cars.manufacturer.ilike(f'%{cid}%'))
        elif filter_type == "Model":
            query = query.filter(Cars.model.ilike(f'%{cid}%'))
        elif filter_type == "Color":
            query = query.filter(Cars.color.ilike(f'%{cid}%'))
        elif filter_type == "Price (Maximum)":
            try:
                max_price = float(cid)
                query = query.filter(Cars.price <= max_price)
            except ValueError:
                flash("Invalid price value. Please enter a number.", "warning")
                query = Cars.query.all()
        elif filter_type == "Price (Minimum)":
            try:
                min_price = float(cid)
                query = query.filter(Cars.price >= min_price)
            except ValueError:
                flash("Invalid price value. Please enter a number.", "warning")
                query = Cars.query.filter(False)
        elif filter_type == "Mileage (Maximum)":
            try:
                max_km = int(cid)
                query = query.filter(Cars.kmcount <= max_km)
            except ValueError:
                flash("Invalid mileage value. Please enter a whole number.", "warning")
                query = Cars.query.filter(False)
        elif filter_type == "Mileage (Minimum)":
            try:
                min_km = int(cid)
                query = query.filter(Cars.kmcount >= min_km)
            except ValueError:
                flash("Invalid mileage value. Please enter a whole number.", "warning")
                query = Cars.query.filter(False)
        else:
            pass

    if not cid or not filter_type:
        cars_list = Cars.query.all()
    else:
        cars_list = query.all()

    is_admin = False
    token = request.cookies.get('access_token')
    if token:
        try:
            #public_key = current_app.config['PUBLIC_KEY']
            #claims = jwt.decode(token, public_key)
            #user_roles = [r['role_name'] for r in claims.get('roles', [])]
            #if "Administrator" in user_roles:
            #    is_admin = True
            if 'Administrator' in session['role']:
                is_admin = True

        except Exception as ex:
            print(f"Failed to decode token for /cars route roles check: {ex}")
            is_admin = False

    return render_template('cars.html', values=cars_list)

# --- Admin page (if signed in as Administrator)
@main_bp.route('/admin/', methods=['GET'], strict_slashes=False)
def admin_page():
    if "role" in session:
       role = session["role"]
       if not "Administrator" in role:
           return redirect(url_for("main.home")) 
    else:
        return redirect(url_for("main.home"))
    
    cid = request.args.get('cid', type=str)
    filter_type = request.args.get('type', type=str)

    query = Cars.query

    if cid and filter_type:
        if filter_type == "Numberplate":
            query = query.filter(Cars.numberplate.ilike(f'%{cid}%'))
        elif filter_type == "Manufacturer":
            query = query.filter(Cars.manufacturer.ilike(f'%{cid}%'))
        elif filter_type == "Model":
            query = query.filter(Cars.model.ilike(f'%{cid}%'))
        elif filter_type == "Color":
            query = query.filter(Cars.color.ilike(f'%{cid}%'))
        elif filter_type == "Price (Maximum)":
            try:
                max_price = float(cid)
                query = query.filter(Cars.price <= max_price)
            except ValueError:
                flash("Invalid price value. Please enter a number.", "warning")
                query = Cars.query.all()
        elif filter_type == "Price (Minimum)":
            try:
                min_price = float(cid)
                query = query.filter(Cars.price >= min_price)
            except ValueError:
                flash("Invalid price value. Please enter a number.", "warning")
                query = Cars.query.filter(False)
        elif filter_type == "Mileage (Maximum)":
            try:
                max_km = int(cid)
                query = query.filter(Cars.kmcount <= max_km)
            except ValueError:
                flash("Invalid mileage value. Please enter a whole number.", "warning")
                query = Cars.query.filter(False)
        elif filter_type == "Mileage (Minimum)":
            try:
                min_km = int(cid)
                query = query.filter(Cars.kmcount >= min_km)
            except ValueError:
                flash("Invalid mileage value. Please enter a whole number.", "warning")
                query = Cars.query.filter(False)
        else:
            pass

    if not cid or not filter_type:
        cars_list = Cars.query.all()
    else:
        cars_list = query.all()

    return render_template('cars_admin.html', values=cars_list, is_admin=True)


# --- Terminate session
@main_bp.route("/logout/")
def logout():
    response = make_response(redirect(url_for("main.home")))

    # Clear Flask server-side session data and JWT access_token cookie
    if "user" in session:
        session.pop("user", None)
    if "role" in session:
        session.pop("role", None)

    response.delete_cookie('access_token')

    flash("You're logged out!", "info")
    return response

# --- User account page (if signed in)
@main_bp.route("/account/")
def account():
   if "user" in session:
       user = session["user"]
       found_user = db.session.query(Users).filter_by(username=user).first()
       if found_user:
           return render_template('account.html', userAccount=found_user)
       else:
           return redirect(url_for("main.home"))
   else:
       return redirect(url_for("main.home"))
   
@main_bp.route("/rentals/")
def rentals():
   if "user" in session:
       user = session["user"]
       found_user = db.session.query(Users).filter_by(username=user).first()
       if found_user:
           token = request.cookies.get('access_token')
           data = verify_token(token)
           if not data:
               return redirect(url_for("main.home"))
           
           rentals_list = requests.get('http://localhost:5000/rental/view_rentals_user', headers=set_auth_headers(token))
           return render_template('rentals2.html', userAccount=found_user, rentals_list=rentals_list.json())
       else:
           return redirect(url_for("main.home"))
   else:
       return redirect(url_for("main.home"))

# --- List all roles
@main_bp.get('/list_roles')
def list_all_roles():
    roles = Roles.query.all()
    return {"roles": [r.role_name for r in roles]}