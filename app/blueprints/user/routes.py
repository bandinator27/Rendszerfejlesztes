from app.blueprints import role_required
from app.blueprints.user import user_bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema
from app.blueprints.user.schemas import UserLoginSchema
from app.blueprints.user.schemas import RoleSchema
from apiflask import HTTPError
from app.blueprints.user.service import UserService
from app.extensions import auth
from flask import redirect, url_for, request, flash

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

# --- MYROLES
@user_bp.get('/myroles')
@user_bp.doc(tags=["user"])
@user_bp.output(RoleSchema(many=True))
@user_bp.auth_required(auth)
def user_list_roles():
    success, response = UserService.get_user_role(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.get('/list_users')
@user_bp.doc(tags=["user"])
@user_bp.auth_required(auth)
@role_required(["Clerk", "Administrator"])
@user_bp.output(UserResponseSchema(many = True))
def user_view():
    success, response = UserService.list_users()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.get('/get_user_data/<string:uid>')
@user_bp.doc(tags=["user"])
@user_bp.output(UserResponseSchema())
@user_bp.auth_required(auth)
#@role_required(["User"])
#@role_required(["Clerk", "Administrator"])
def get_user_data(uid):
    success, response = UserService.get_user_data(uid)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --- EDIT USER DATA
@user_bp.post('/set_user_data/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.input(UserRequestSchema, location="json")
@user_bp.auth_required(auth)
@role_required(["User", "Clerk", "Administrator"])
def set_user_data(uid, json_data):
    current_user_id = auth.current_user.get("user_id")
    if current_user_id != uid and not set(auth.current_user.get("roles", [])) & {"Administrator"}:
        raise HTTPError(message="You can only modify your own data. The ID belongs to someone else.", status_code=403)
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
        }
    }
    success, response = UserService.set_user_data(uid, json_data)
    if success:
        flash(response, "success")
        return redirect(url_for("main.account"))
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