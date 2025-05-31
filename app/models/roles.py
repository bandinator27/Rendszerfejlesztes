from app.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey
from typing import List
from app.models.users import UserRole

class Roles(db.Model):
    __tablename__ = "Roles"
    #id: Mapped[int] = mapped_column(ForeignKey("Users.id"), primary_key=True)
    #role_name: Mapped[str] = mapped_column(String(32), primary_key=True)

    id: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str] = mapped_column(String(30)) 
    users : Mapped[List["Users"]] = relationship(secondary=UserRole, back_populates="roles")
    
    # def __repr__(self) -> str:
    #     return f"Roles (id={self.id!r}, name={self.name!s})"