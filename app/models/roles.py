from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from typing import List
from app.models.users import Users, UserRole

class Roles(db.Model):
    __tablename__ = "Roles"
    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(30)) 
    users : Mapped[List["Users"]] = relationship(secondary=UserRole, back_populates="roles")