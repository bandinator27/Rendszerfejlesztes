from flask import redirect, url_for, render_template, request, session, flash, make_response
from app.extensions import db
from app.models.addresses import Addresses
from app.blueprints.user.schemas import PayloadSchema, RoleSchema
from app.blueprints import main_bp, verify_token, set_auth_headers
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *
from werkzeug.security import generate_password_hash
from sqlalchemy import select
from app.forms.loginform import LoginForm
from app.forms.registerform import RegisterForm
import requests

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
        login_request = requests.post('http://localhost:5000/user/login',
                        json={
                            'username': form.username.data,
                            'password': form.password.data
                        })

        login_response = login_request.json()

        print(f"Login API Status Code: {login_request.status_code}")
        print(f"Login API Response Text: {login_request.text}")

        if not login_response["token"]:
            flash("Wrong username or password!", "danger")
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
        resp.set_cookie('access_token', login_response["token"])
            
        flash("You're signed in!", "info")
        return resp

    return render_template('login.html', name='Sign In', form=form)

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
    if session["user"]:
        if "Administrator" in session["role"]:
            token = request.cookies.get('access_token')
            users = requests.get('http://localhost:5000/user/list_users', headers=set_auth_headers(token))
            print(users.json())
            #return redirect(url_for("main.home"))
            roles = []
            for user in users.json():
               user_data = requests.get('http://localhost:5000/user/get/roles/'+str(user["id"]), headers=set_auth_headers(token))
               data = ''
               for role in user_data.json():
                   if not len(data) < 1:
                       data = data + ', ' + role['role_name']
                   else:
                       data = role['role_name']
               roles.append(data)

            print(roles)
            return render_template('view.html', users=users.json(), roles=roles)
    return redirect(url_for("main.home")) 

# --- List cars
@main_bp.route('/cars', methods=['GET'], strict_slashes=False)
def cars():
    cid = request.args.get('cid', type=str)
    filter_type = request.args.get('type', type=str)

    if not filter_type:
        filter_type = 'default'

    if not cid:
        cid = 'default'

    filter_request = requests.post('http://localhost:5000/car/filter/',
    json={
        'filter_type': filter_type,
        'filterValue': cid
    })

    cars_list = []
    for car in filter_request.json():
        cars_list.append(car)
      
    return render_template('cars.html', cars_list=cars_list)

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

    if not filter_type:
        filter_type = 'default'

    if not cid:
        cid = 'default'

    filter_request = requests.post('http://localhost:5000/car/filter/',
    json={
        'filter_type': filter_type,
        'filterValue': cid
    })

    cars_list = []
    for car in filter_request.json():
        cars_list.append(car)

    return render_template('cars_admin.html', cars_list=cars_list, is_admin=True)

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
            token = request.cookies.get('access_token')
            data = verify_token(token)
            if not data:
               return redirect(url_for("main.home"))
           
            rentals_list = requests.get('http://localhost:5000/rental/view_rentals_user', headers=set_auth_headers(token))
            numberplates = []
            for rental in rentals_list.json():
               car_data = requests.get('http://localhost:5000/car/view/'+str(rental["carid"]), headers=set_auth_headers(token))
               numberplates.append(car_data.json()['numberplate'])

            return render_template('account.html', userAccount=found_user, rentals_list=rentals_list.json(), numberplates=numberplates)
        else:
           return redirect(url_for("main.home"))
    else:
       return redirect(url_for("main.home"))