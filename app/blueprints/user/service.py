from app.database import db
from app.blueprints.user.schemas import UserResponseSchema
from app.models.users import Users
from app.models.addresses import Addresses
from app.models.roles import Roles

from sqlalchemy import select

class UserService:

    @staticmethod
    def user_registrate(request):
        try:
            if db.session.execute(select(Users).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "E-mail already exist!"
            
            request["address"] = Addresses(**request["address"])
            user = Users(**request)
            #user.roles.append(
            #    db.session.execute(select(Roles).filter_by(name="User")).scalar_one()
            #)
            #db.session.add(user)
            #db.session.commit()

        except Exception as ex:
            return False, "Incorrect User data!"
        return True, UserResponseSchema().dump(user)
    
    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(Users).filter_by(email=request["email"])).scalar_one()
            if not user.check_password(request["password"]):
                return False, "Incorrect e-mail or password!"
            
        except Exception as ex:
            return False, "Incorrect Login data!"
        return True, UserResponseSchema().dump(user)