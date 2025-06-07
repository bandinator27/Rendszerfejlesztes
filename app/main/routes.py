from flask import redirect, url_for, render_template, request, session, flash
from app.extensions import db
from app.models.addresses import Addresses
from app.blueprints import main_bp, user_bp
from app.models.cars import *
from app.models.rentals import *
from app.models.roles import *
from app.models.users import *
from werkzeug.security import check_password_hash
from sqlalchemy import select
from werkzeug.security import generate_password_hash

@main_bp.route("/")
def home():
   if "user" in session:
       user = session["user"]
   else:
       user = "None"
   return render_template('index.html', user = user)

@main_bp.route("/login/", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = db.session.query(Users).filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username

            # Determine primary role
            all_roles_ordered_by_id = db.session.execute(select(Roles).order_by(Roles.id.desc())).scalars().all()
            role_hierarchy = [role.role_name for role in all_roles_ordered_by_id]
            user_role_names = [role.role_name for role in user.roles]
            primary_role = next((r for r in role_hierarchy if r in user_role_names), None)
            session['role'] = primary_role

            from authlib.jose import jwt
            from datetime import datetime, timedelta
            from flask import make_response, current_app
            from app.blueprints.user.schemas import PayloadSchema, RoleSchema

            payload = PayloadSchema()
            payload.user_id = user.id
            payload.roles = RoleSchema().dump(obj=user.roles, many=True)
            payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())

            header = {'alg': 'RS256'}
            claims = PayloadSchema().dump(payload)
            private_key = current_app.config['SECRET_KEY']
            token = jwt.encode(header, claims, private_key).decode()

            resp = make_response(redirect(url_for('main.home')))
            resp.set_cookie('access_token', token, httponly=True, secure=False, samesite='Lax')
            
            flash("You're signed in!", "info")
            return resp

        else:
            flash("Incorrect sign-in details!", "danger")
            return render_template('login.html', register=url_for('main.register'))

    return render_template('login.html', register=url_for('main.register'))

# --- Login
#@main_bp.route("/login/", methods=['GET', 'POST'])
#def login():
#    if request.method == 'POST':
#        username = request.form.get('username')
#        password = request.form.get('password')
#        user = db.session.query(Users).filter_by(username=username).first()
#
#        if user and check_password_hash(user.password, password):
#            session['user'] = user.username
#
#            # Determine primary role
#            all_roles_ordered_by_id = db.session.execute(select(Roles).order_by(Roles.id.desc())).scalars().all()
#            role_hierarchy = [role.role_name for role in all_roles_ordered_by_id]
#            user_role_names = [role.role_name for role in user.roles]
#            primary_role = next((r for r in role_hierarchy if r in user_role_names), None)
#            session['role'] = primary_role
#
#            from authlib.jose import jwt
#            from datetime import datetime, timedelta
#            from flask import make_response, current_app
#            from app.blueprints.user.schemas import PayloadSchema, RoleSchema
#
#            payload = PayloadSchema()
#            payload.user_id = user.id
#            payload.roles = RoleSchema().dump(obj=user.roles, many=True)
#            payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
#
#            header = {'alg': 'RS256'}
#            claims = PayloadSchema().dump(payload)
#            private_key = current_app.config['SECRET_KEY']
#            token = jwt.encode(header, claims, private_key).decode('utf-8')
#
#            resp = make_response(redirect(url_for('main.home')))
#            resp.set_cookie('access_token', token, httponly=True, secure=False, samesite='Lax')
#            
#            flash("You're signed in!", "info")
#            return resp
#
#        else:
#            flash("Incorrect sign-in details!", "danger")
#            return render_template('login.html', register=url_for('main.register'))
#
#    return render_template('login.html', register=url_for('main.register'))


# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         user = db.session.query(Users).filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['user'] = user.username

#             # if the user has multiple roles, determine the primary role based on the hierarchy
#             # the higher the role id, the more important it is
#             all_roles_ordered_by_id = db.session.execute(select(Roles).order_by(Roles.id.desc())).scalars().all()
#             role_hierarchy = [role.role_name for role in all_roles_ordered_by_id]
            
#             user_role_names = [role.role_name for role in user.roles]

#             primary_role = None
#             for role_in_hierarchy in role_hierarchy:
#                 if role_in_hierarchy in user_role_names:
#                     primary_role = role_in_hierarchy
#                     break
#             session['role'] = primary_role
#             flash("You're signed in!", "info")
#             return redirect(url_for('main.home'))
#         else:
#             flash("Incorrect sign-in details!", "danger")
#             return render_template('login.html', register=url_for('main.register'))
#     return render_template('login.html', register = url_for('main.register'))

# --- Registration
@main_bp.route("/register/", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        city = request.form.get('city')
        street = request.form.get('street')
        postalcode = request.form.get('postalcode')

        # Create address
        address = Addresses(city=city, street=street, postalcode=postalcode)
        db.session.add(address)
        db.session.commit()

        hashed_password = generate_password_hash(password)

        user = Users(
            username=username,
            password=hashed_password,
            password_salt="",  
            email=email,
            address_id=address.id,
            phone_number=phone_number
        )
        db.session.add(user)
        db.session.commit()

        flash("Successful registration! You can now sign in.", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html')

# --- List users for testing
@main_bp.route("/view/")
def view():
   return render_template('view.html', values=db.session.query(Users).all())

# --- List cars for testing
@main_bp.route('/cars', methods=['GET'], strict_slashes=False)
def cars():
    cid = request.args.get('cid', type=str)
    filter_type = request.args.get('type', type=str)

    #if cid:
    #    cars = Cars.query.filter_by(carid=cid).all()
    #else:
    #    cars = Cars.query.all()

    if filter_type == "Numberplate":
        cars = Cars.query.filter_by(numberplate=cid).all()
    elif filter_type == "Manufacturer":
        cars = Cars.query.filter_by(manufacturer=cid).all()
    elif filter_type == "Model":
        cars = Cars.query.filter_by(model=cid).all()
    elif filter_type == "Color":
        cars = Cars.query.filter_by(color=cid).all()
    elif filter_type == "Price (Maximum)":
        cars = db.session.execute(select(Cars).filter(Cars.price <= cid)).scalars().all()
    elif filter_type == "Price (Minimum)":
        cars = db.session.execute(select(Cars).filter(Cars.price >= cid)).scalars().all()
    elif filter_type == "Mileage (Maximum)":
        cars = db.session.execute(select(Cars).filter(Cars.kmcount <= cid)).scalars().all()
    elif filter_type == "Mileage (Minimum)":
        cars = db.session.execute(select(Cars).filter(Cars.kmcount >= cid)).scalars().all()
    else:
        cars = Cars.query.all()

    return render_template('cars.html', values=cars)

# --- Terminate session
@main_bp.route("/logout/")
def logout():
   if "user" in session:
       session.pop("user", None)
       session.pop("role", None)
       flash("You've signed out!", "info")
   return redirect(url_for("main.home"))

# --- Admin page (if signed in as Administrator)
@main_bp.route("/admin/")
def admin_page():
   if "role" in session:
       role = session["role"]
       if role == "Administrator":
           return render_template('admin.html')
       else:
           return redirect(url_for("main.home"))
   else:
       return redirect(url_for("main.home"))

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
           return render_template('rentals.html', userAccount=found_user)
       else:
           return redirect(url_for("main.home"))
   else:
       return redirect(url_for("main.home"))

# --- List all roles
@main_bp.get('/list_roles')
def list_all_roles():
    roles = Roles.query.all()
    return {"roles": [r.role_name for r in roles]}