from app.extensions import db
from app.blueprints.user.schemas import UserResponseSchema, PayloadSchema, RoleSchema
from app.models.users import Users
from app.models.addresses import Addresses
from app.models.roles import Roles
from datetime import datetime, timedelta
from authlib.jose import jwt
from flask import current_app
from sqlalchemy import select
from werkzeug.security import generate_password_hash

class UserService:

# --- Registration
    @staticmethod
    def user_register(request):
        try:
            if db.session.execute(select(Users).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "This email adress is already in use!"
            
            address_data = request.pop("address")
            address = Addresses(**address_data)
            db.session.add(address)
            db.session.commit()

            request["address_id"] = address.id
            request["password"] = generate_password_hash(request["password"])

            user = Users(**request)
            db.session.add(user)
            db.session.commit()
            UserService.add_user_role(user.id, "User")

        except Exception as ex:
            return False, f"Incorrect user data! Details: {ex}"
        return True, {
            "message": "Successful registration!",
            "user": UserResponseSchema().dump(user)
        }

# --- Login
    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(Users).filter(Users.username == request["username"])).scalar_one_or_none()
            
            if user is None:
                return False, {
                    "message": "No user found with this username.",
                    "error_type": "auth_failed"
                }
     
            if not user.check_password(request["password"]):
                return False, {
                    "message": "Incorrect password",
                    "error_type": "auth_failed"
                }
                
            user_schema = UserResponseSchema().dump(user)
            user_schema["token"] = UserService.token_generate(user)
            return True, user_schema   

        except Exception as ex:
            return False, {
                "message": f"Login error: {ex}",
                "error_type": "server_error"
            }

# --- List users
    @staticmethod
    def list_users():
        try:
            user = db.session.query(Users).all()
        except Exception as ex:
            return False, f"Database error! (user_view) Details: {ex}"
        return True, UserResponseSchema().dump(user, many=True)

# --- Token generation
    @staticmethod
    def token_generate(user : Users):
        print(f"DEBUG: Generating token for user {user.username}")
        payload = PayloadSchema()
        payload.user_id = user.id
        payload.roles = RoleSchema().dump(obj=user.roles, many=True)
        payload.exp = int((datetime.now()+ timedelta(minutes=30)).timestamp())
        
        return jwt.encode({'alg': 'RS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()
   
    @staticmethod
    def get_user_data(user_id):
        user = db.session.execute(select(Users).filter(Users.email == user_id)).scalar_one_or_none()
        if user is None:
            return False, "User not found! (get_user_data)"
        return True, UserResponseSchema().dump(user)
    
    @staticmethod
    def set_user_data(user_id, request):
        try:
            user = db.session.get(Users, user_id)
            if user:
                user.username = request["username"]
                user.email = request["email"]
                user.set_password(request["password"])
                user.phone_number = request["phone_number"]
                address = request["address"]

                addr = db.session.execute(
                    select(Addresses).filter(
                        Addresses.city == address["city"],
                        Addresses.street == address["street"],
                        Addresses.postalcode == address["postalcode"]
                    )).scalar_one_or_none()
                if addr is None:
                    new_address = Addresses(
                        city=address["city"],
                        street=address["street"],
                        postalcode=address["postalcode"]
                    )
                    db.session.add(new_address)
                    db.session.commit()
                    user.address_id = new_address.id
                else:
                    user.address_id = addr.id

                db.session.commit()
                return True, "You've successfully updated your details!"
            else:
                return False, "User not found."
        except Exception as ex:
            db.session.rollback()  # Rollback on error
            return False, f"Database error! (set_user_data) Details: {ex}"

    @staticmethod
    def add_user_role(user_id, role_name):
        try:
            role = Roles(id=user_id, role_name=role_name)
            db.session.add(role)
            db.session.commit()
            return True, RoleSchema().dump(role)
        except Exception as ex:
            db.session.rollback()  # Rollback on error
            return False, f"Database error! (add_user_role) Details: {ex}"
        
    @staticmethod
    def remove_user_role(user_id, role_name):
        try:
            role = db.session.execute(select(Roles).filter(Roles.id == user_id, Roles.role_name == role_name)).scalar_one()
            db.session.commit()
            return True, RoleSchema().dump(role)
        except Exception as ex:
            return False, f"Database error! (remove_user_role) Details: {ex}"

    @staticmethod
    def get_user_role(user_id):
        roles = db.session.execute(select(Roles.role_name).filter(Roles.id==user_id)).scalars().all()
        if not roles:
            return True, []
        role_dicts = [{"role_name": r} for r in roles]
        return True, RoleSchema(many=True).dump(role_dicts)