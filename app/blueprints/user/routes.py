from app.blueprints import role_required, set_auth_headers, verify_token
from app.blueprints.user import user_bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema, UserLoginSchema, RoleSchema, UserFilterSchema
from apiflask import HTTPError
from app.blueprints.user.service import UserService
from app.extensions import auth
from flask import redirect, url_for, request, flash, session, render_template, make_response
import requests

# @user_bp.route('/')
# def index():
#     return 'This is the users Blueprint'

# --- LOGIN (redirected to main.login)
@user_bp.post('/login')
@user_bp.doc(tags=["user"])
@user_bp.input(UserLoginSchema, location="json")
def user_login(json_data):
     print(json_data)
     success, response = UserService.user_login(json_data)
     if success:
         return response, 200
     raise HTTPError(message=response, status_code=400)

# --- REGISTER
@user_bp.post('/register')
@user_bp.input(UserRequestSchema, location="json")
@user_bp.output(UserResponseSchema)
def user_register(json_data):
    success, response = UserService.user_register(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- GET USER ROLES
@user_bp.get('/get/roles/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.output(RoleSchema(many=True))
@user_bp.auth_required(auth)
@role_required(["Administrator"])
def user_list_roles(uid):
    success, response = UserService.get_user_role(uid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.post('/list_users')
@user_bp.doc(tags=["user"])
@user_bp.input(UserFilterSchema, location="json")
@user_bp.auth_required(auth)
@role_required(["Administrator"])
@user_bp.output(UserResponseSchema(many = True))
def user_view(json_data):
    success, response = UserService.list_users(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.get('/get/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.output(UserResponseSchema())
@user_bp.auth_required(auth)
@role_required(["Administrator", "Clerk"])
def get_user_data(uid):
    success, response = UserService.get_user_data(uid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.get('/get/self')
@user_bp.doc(tags=["user"])
@user_bp.output(UserResponseSchema())
@user_bp.auth_required(auth)
def get_user_data_self():
    success, response = UserService.get_user_data(auth.current_user.get('user_id'))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- EDIT USER DATA
@user_bp.post('/set_user_data/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.input(UserRequestSchema, location="json")
@user_bp.auth_required(auth)
@role_required(["Administrator"])
def set_user_data(uid, json_data):
    current_user_id = auth.current_user.get("user_id")
    if current_user_id != uid and not set(auth.current_user.get("roles", [])) & {"Administrator"}:
        raise HTTPError(message="You can only edit your own data.", status_code=403)
    success, response = UserService.set_user_data(uid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.post('/edit/<int:uid>')
@user_bp.doc(tags=["user"])
def edit_user_data(uid):
    form = request.form
    json_data = {
        "username": form.get("username"),
        "email": form.get("email"),
        "password": form.get("password"),
        "phone_number": form.get("phone_number"),
        "address": {
            "postalcode": form.get("postalcode"),
            "city": form.get("city"),
            "street": form.get("street")
        }}

    if not session['user_id']:
        flash("You are not logged in!", "warning")
        return redirect(url_for("main.account"))

    if session['user_id'] != uid and not 'Administrator' in session['role']:
        flash("You can't edit someone else's account!", "warning")
        return redirect(url_for("main.account"))
    
    success, response = UserService.set_user_data(uid, json_data)
    if success:
        flash(response, "success")
        session.clear()
        
        resp = make_response(redirect(url_for("main.login")))
        resp.delete_cookie('access_token')
        flash("Your info has been updated. Please sign in again with your new credentials.", "info")
        return resp

    else:
        flash(response, "warning")
        return redirect(url_for("main.account"))

# @user_bp.post('/remove_role/<int:uid>')
# @user_bp.doc(tags=["user"])
# @user_bp.input(RoleSchema, location="json")
# @user_bp.auth_required(auth)
# #@role_required(["User"])
# #@role_required(["Clerk", "Administrator"])
# def remove_user_role(uid, json_data):
#     success, response = UserService.remove_user_role(uid, json_data)
#     if success:
#         return response, 200
#     raise HTTPError(message=response, status_code=400)

# --- List users for testing
@user_bp.route("/view_users")
def view_users():
    if session["user"]:
        if "Administrator" in session["role"]:
            cid = request.args.get('cid', type=str)
            filter_type = request.args.get('type', type=str)

            if not filter_type:
                filter_type = 'default'

            if not cid:
                cid = 'default'

            token = request.cookies.get('access_token')
            response = requests.post('http://localhost:5000/user/list_users',
            json={
                'filter_type': filter_type,
                'filterValue': cid
            }, headers=set_auth_headers(token))

            users = response.json()

            if response.status_code != 200:
                users = []

            roles = []
            for user in users:
               user_data = requests.get('http://localhost:5000/user/get/roles/'+str(user["id"]), headers=set_auth_headers(token))
               data = ''
               for role in user_data.json():
                   if not len(data) < 1:
                       data = data + ', ' + role['role_name']
                   else:
                       data = role['role_name']
               roles.append(data)

            return render_template('view.html', users=users, roles=roles)
    return redirect(url_for("main.home"))

# --- Invoice
@user_bp.route("/invoice/<int:cid>")
def invoice(cid):

    if not session['user_id']:
        flash("You are not logged in!", "danger")
        return redirect(url_for("main.account"))
    
    token = request.cookies.get('access_token')
    data = verify_token(token)
    if not data:
        return redirect(url_for("main.home"))
           
    response = requests.get('http://localhost:5000/rental/get/user/'+str(cid), headers=set_auth_headers(token))
    rental_data = response.json()

    if response.status_code != 200:
        return redirect(url_for("main.account"))
    
    if rental_data['rentstatus'] == 'Pending':
        return redirect(url_for("main.account"))

    car_data = requests.get('http://localhost:5000/car/view/'+str(rental_data["carid"]), headers=set_auth_headers(token))
    numberplate = car_data.json()['numberplate']

    user_data = requests.get('http://localhost:5000/user/get/self', headers=set_auth_headers(token))
    username = user_data.json()['username']
    
    from flask import send_file
    from io import BytesIO
    from reportlab.pdfgen import canvas
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Create a PDF document
    p.drawString(100, 750, "Car Rental - Invoice")

    y = 700
    p.drawString(100, y, f"Username: {username}")
    p.drawString(100, y - 20, f"Numberplate: {numberplate}")
    p.drawString(100, y - 40, f"Rent start-date: {rental_data['rentstart']}")
    p.drawString(100, y - 60, f"Rent status: {rental_data['rentstatus']}")
    p.drawString(100, y - 80, f"Rent duration: {rental_data['rentduration']} days")
    p.drawString(100, y - 100, f"Rent price: {rental_data['rentprice']}$")
    p.drawString(100, y - 120, f"Address: {rental_data['renteraddress']}")
    p.drawString(100, y - 140, f"Phone number: {rental_data['renterphonenum']}")
    y -= 60

    p.showPage()
    p.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=numberplate+'-'+rental_data['rentstart']+'-invoice.pdf')