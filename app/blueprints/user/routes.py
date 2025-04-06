from app.blueprints.user import user_bp
from app.blueprints.user.schemas import UserRequestSchema, UserResponseSchema
from app.blueprints.user.schemas import UserLoginSchema
from apiflask import HTTPError
from app.blueprints.user.service import UserService

@user_bp.route('/')
def index():
    return 'This is the user Blueprint'

@user_bp.post('/registrate')
@user_bp.input(UserRequestSchema, location="json")
@user_bp.output(UserResponseSchema)
def user_registrate(json_data):
    success, response = UserService.user_registrate(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)

@user_bp.post('/login')
@user_bp.doc(tags=["user"])
@user_bp.input(UserLoginSchema, location="json")
@user_bp.output(UserResponseSchema)
def user_login(json_data):
    success, response = UserService.user_login(json_data)
    if success:
        return response, 200
    raise HTTPError(message=response, status_code=400)