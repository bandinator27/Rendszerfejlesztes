from flask import redirect, url_for, render_template, request, session, flash, make_response
from app.extensions import db
from app.blueprints import main_bp, verify_token, set_auth_headers
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *
from werkzeug.security import generate_password_hash
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

        if login_request.status_code != 200:
            flash("Incorrect username or password. Please try again!", "danger")
            return render_template('login.html', name='Sign In', form=form)
        
        login_response = login_request.json()

        if not login_response["token"]:
            flash("Incorrect username or password. Please try again!", "danger")
            return redirect("/login")
        
        session['user'] = login_response["username"]
        session['user_id'] = login_response["id"]

        data = verify_token(login_response["token"])

        role_list = []
        for role in data["roles"]:
            role_list.append(role['role_name'])

        session['role'] = role_list
        print(session['role'])
        if 'Administrator' in session.get('role'):
            print('Admin yaaay!')
        if 'User' in session.get('role'):
            print('User yaay!')
        if 'Clerk' in session.get('role'):
            print('Clerk yaay!')

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
    if "user_id" in session:
        session.pop("id", None)

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