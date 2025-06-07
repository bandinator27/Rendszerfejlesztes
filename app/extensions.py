from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from apiflask import HTTPTokenAuth

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
auth = HTTPTokenAuth(scheme='Bearer')