from app.database import db
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

    @staticmethod
    def user_register(request):
        try:
            if db.session.execute(select(Users).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "A megadott e-mail cím már létezik!"
            
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
            return False, f"Hibás felhasználói adatok! ({ex})"
        return True, {
            "message": "Sikeres regisztráció!",
            "user": UserResponseSchema().dump(user)
        }
    
    @staticmethod
    def user_login(request):
        #try:
        user = db.session.execute(select(Users).filter(Users.email == request["email"])).scalar_one_or_none()
            #if user is None:
            #    user = db.session.execute(select(Users).filter_by(Users.username == request["email"])).scalar_one_or_none()
            #    if user is None:
            #        return False, "Incorrect e-mail/username or password!"
                
        if not user.check_password(request["password"]):
            return False, "Helytelen felhasználónév vagy jelszó!"
            
        user_schema = UserResponseSchema().dump(user)
        user_schema["token"] = UserService.token_generate(user)
        return True, UserResponseSchema().dump(user_schema)   
        #except Exception as ex:
        #    return False, "Incorrect login data!"
    
    @staticmethod
    def user_view():
        try:
            #user = db.session.execute(select(Users).filter(Users.id==1)).scalar_one()
            user = db.session.query(Users).all()
            
        except Exception as ex:
            return False, f"Hibás bejelentkezési adatok! ({ex})"
        return True, UserResponseSchema().dump(user, many = True)
    
    @staticmethod
    def token_generate(user : Users):
        payload = PayloadSchema()
        payload.exp = int((datetime.now()+timedelta(minutes=30)).timestamp())
        payload.user_id = user.id
        roles = db.session.execute(select(Roles).filter(Roles.id == user.id, Roles.role_name == "Administrator")).scalar_one_or_none()
        if roles is None:
            roles = db.session.execute(select(Roles).filter(Roles.id == user.id, Roles.role_name == "Clerk")).scalar_one_or_none()
            if roles is None:
                roles = db.session.execute(select(Roles).filter(Roles.id == user.id, Roles.role_name == "User")).scalar_one_or_none()
                if roles is None:
                    payload.roles = ["None"]
                else:
                    payload.roles = ["User"]
            else:
                payload.roles = ["Clerk"]
        else:
            payload.roles = ["Administrator"]

        return jwt.encode({'alg': 'HS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()
    
    @staticmethod
    def list_roles(user_id):
        #roles = db.session.get(Roles, user_id)
        roles = db.session.execute(select(Roles).filter(Roles.id==user_id)).scalars()
        #roles = db.session.query(Roles).all()
        if roles is None:
            return False, "User not found!"
        
        return True, RoleSchema().dump(roles, many = True)
    
    @staticmethod
    def get_user_data(user_id):
        user = db.session.execute(select(Users).filter(Users.email == user_id)).scalar_one_or_none()
        if user is None:
            return False, "User not found!"
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
                address = request["Address"]
                addr = db.session.execute(select(Addresses).filter(Addresses.city == address.city,
                   Addresses.street == address.street,
                   Addresses.postalcode == address.postalcode)).scalar_one_or_none()
                if addr is None:
                    new_address = Addresses(address.city, address.street, address.postalcode)
                    db.session.add(new_address)
                    db.session.commit()
                else:
                    user.address_id = addr.id

                db.session.commit()

        except Exception as ex:
            return False, f"Váratlan hiba történt! ({ex})"

    @staticmethod
    def add_user_role(user_id, role_name):
        try:
            roles = Roles(user_id, role_name)
            db.session.add(roles)
            db.session.commit()
            return True, RoleSchema().dump(roles)
        
        except Exception as ex:
            return False, "Adatbázis hiba"
        
    @staticmethod
    def remove_user_role(user_id, role_name):
        try:
            roles = db.session.execute(select(Roles).filter(Roles.id == user_id, Roles.role_name == role_name)).scalar_one()
            db.session.commit()
            return True, RoleSchema().dump(roles)
        
        except Exception as ex:
            return False, "Adatbázis hiba"
        
    @staticmethod
    def get_user_roles(user_id):
        roles = db.session.execute(select(Roles).filter(Roles.id==user_id)).scalars()

        if roles is None:
            return False, "A felhasználó vagy a szerepkör nem található!"
        
        return True, RoleSchema().dump(roles, many = True)