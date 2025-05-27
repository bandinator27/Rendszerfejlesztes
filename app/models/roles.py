from app.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey

class Roles(db.Model):
    __tablename__ = "Roles"
    id: Mapped[int] = mapped_column(ForeignKey("Users.id"), primary_key=True)
    role_name: Mapped[str] = mapped_column(String(32), primary_key=True)

    #id: Mapped[int] = mapped_column(primary_key=True)
    #role_name: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
