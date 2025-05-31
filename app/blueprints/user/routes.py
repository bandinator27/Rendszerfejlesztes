from app.blueprints.user import user_bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema
from app.blueprints.user.schemas import UserLoginSchema
from app.blueprints.user.schemas import RoleSchema
from apiflask import HTTPError
from app.blueprints.user.service import UserService
from app.database import auth

# @user_bp.route('/')
# def index():
#     return 'This is the users Blueprint'

# --- LOGIN
@user_bp.post('/login')
@user_bp.doc(tags=["user"])
@user_bp.input(UserLoginSchema, location="json")
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    return response, 401

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
#@role_required(["User"])
def user_list_roles():
    success, response = UserService.list_roles(auth.current_user.get("user_id"))
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# --ADD_ROLE - not in netpincer example
# @user_bp.post('/add_role/<int:uid>')
# @user_bp.doc(tags=["user"])
# @user_bp.input(RoleSchema, location="json")
# @user_bp.auth_required(auth)
# def add_user_role(uid, json_data):
#     role_name = json_data.get('role_name')
#     if not role_name: # egyszerű ellenőrzés, szerepkör neve benne van-e a kapott JSON-ban
#         raise HTTPError(message="A szerepkör hiányzik!", status_code=400)
#     success, response = UserService.add_user_role(user_id=uid, role_name=role_name)
#     if success:
#         return response, 200
#     raise HTTPError(message = response, status_code = 400)

# def add_user_role(uid, json_data):
#     success, response = UserService.add_user_role(uid, json_data)
#     if success:
#         return response, 200
#     raise HTTPError(message=response, status_code=400)

#@role_required(["User"])
#@role_required(["Clerk", "Administrator"])

@user_bp.get('/user_view')
@user_bp.doc(tags=["user"])
@user_bp.output(UserResponseSchema(many = True))
def user_view():
    success, response = UserService.user_view()
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

# összes role listázása
@user_bp.post('/roles')
@user_bp.doc(tags=["user"])
@user_bp.output(RoleSchema(many = True))
#@role_required(["User"])
#@role_required(["Clerk", "Administrator"])
def user_list_all_roles():
    success, response = UserService.list_roles(1)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.get('/user_data/<string:uid>')
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

@user_bp.post('/user_data/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.input(UserRequestSchema, location="json")
@user_bp.auth_required(auth)
#@role_required(["User"])
#@role_required(["Clerk", "Administrator"])
def set_user_data(uid, json_data):
    success, response = UserService.set_user_data(uid, json_data)
    if success:
        return response, 200
    raise HTTPError(message = response, status_code = 400)

@user_bp.post('/remove_role/<int:uid>')
@user_bp.doc(tags=["user"])
@user_bp.input(RoleSchema, location="json")
@user_bp.auth_required(auth)
#@role_required(["User"])
#@role_required(["Clerk", "Administrator"])
def remove_user_role(uid, json_data):
    success, response = UserService.remove_user_role(uid, json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)