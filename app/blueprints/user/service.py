from app.extensions import db
from app.blueprints.user.schemas import UserResponseSchema, PayloadSchema, RoleSchema
from app.models.users import Users
from app.models.addresses import Addresses
from app.models.roles import Roles
from datetime import datetime, timedelta
from authlib.jose import jwt
from flask import current_app
from sqlalchemy import select

class UserService:

# --- Registration
    @staticmethod
    def user_register(request):
        try:
            if db.session.execute(select(Users).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "This email address is already in use!"
            
            if db.session.execute(select(Users).filter_by(username=request["username"])).scalar_one_or_none():
                return False, "This username is already in use!"
            
            address_data = request.pop("address")
            address = Addresses(**address_data)
            db.session.add(address)
            db.session.commit()

            request["address_id"] = address.id
            request["password_salt"] = request["username"][::-1]

            user = Users(**request)
            db.session.add(user)
            db.session.commit()

            new_user = db.session.execute(select(Users).filter_by(username=request["username"])).scalar_one_or_none()
            UserService.add_user_role(new_user.id, "User")

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
     
            if not user.check_password(request["username"][::-1]+request["password"]):
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
    def list_users(request):
        filter_type = request['filter_type']
        filterValue = request['filterValue']
        try:
            query = Users.query
            if filter_type:
                if filter_type == "Username":
                    query = query.filter(Users.username.ilike(f'%{filterValue}%'))
                elif filter_type == "Email":
                    query = query.filter(Users.email.ilike(f'%{filterValue}%'))
                elif filter_type == "Address":
                    addresses = db.session.execute(select(Addresses).filter(Addresses.city.ilike(f'%{filterValue}%'))).scalars().all()
                    user = []
                    for address in addresses:
                        user_req = db.session.execute(select(Users).filter(Users.address_id==address.id)).scalar_one_or_none()
                        user.append(user_req)

                    print(user)

                    addresses = db.session.execute(select(Addresses).filter(Addresses.postalcode.ilike(f'%{filterValue}%'))).scalars().all()
                    for address in addresses:
                        user_req = db.session.execute(select(Users).filter(Users.address_id==address.id)).scalar_one_or_none()
                        user.append(user_req)

                    print(user)

                    addresses = db.session.execute(select(Addresses).filter(Addresses.street.ilike(f'%{filterValue}%'))).scalars().all()
                    for address in addresses:
                        user_req = db.session.execute(select(Users).filter(Users.address_id==address.id)).scalar_one_or_none()
                        user.append(user_req)
                    
                    print(user)

                    list(set(user))
                    print(user)

                elif filter_type == "Phone number":
                    query = query.filter(Users.phone_number.ilike(f'%{filterValue}%'))
                elif filter_type == "Roles":
                    roles = db.session.execute(select(Roles).filter(Roles.role_name.ilike(f'%{filterValue}%'))).scalars().all()
                    user = []
                    for role in roles:
                        user_req = db.session.execute(select(Users).filter(Users.id==role.id)).scalar_one_or_none()
                        user.append(user_req)
                else:
                    pass

            if not filterValue or not filter_type:
                user = Users.query.all()
            else:
                if not filter_type == "Roles" and not filter_type == "Address":
                    user = query.all()

        except Exception as ex:
            return False, f"Database error! (user_view) Details: {ex}"
        return True, UserResponseSchema().dump(user, many=True)

# --- Token generation
    @staticmethod
    def token_generate(user : Users):
        print(f"DEBUG: Generating token for user {user.username}")
        payload = PayloadSchema()
        payload.user_id = user.id
        payload.roles = UserService.get_user_role_internal(user)
        payload.exp = int((datetime.now()+ timedelta(minutes=30)).timestamp())
        
        return jwt.encode({'alg': 'RS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()
   
    @staticmethod
    def get_user_data(user_id):
        user = db.session.execute(select(Users).filter(Users.id == user_id)).scalar_one_or_none()
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
                if request["password"]:
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
                return True, "User data updated successfully. Log in again to apply changes."
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
    def get_user_role(uid):
        roles = db.session.execute(select(Roles.role_name).filter(Roles.id==uid)).scalars().all()
        if not roles:
            return True, []
        role_dicts = [{"role_name": r} for r in roles]
        return True, RoleSchema(many=True).dump(role_dicts)
    
    @staticmethod
    def get_user_role_internal(user):
        roles = db.session.execute(select(Roles.role_name).filter(Roles.id==user.id)).scalars().all()
        if not roles:
            return []
        role_dicts = [{"role_name": r} for r in roles]
        return RoleSchema(many=True).dump(role_dicts)