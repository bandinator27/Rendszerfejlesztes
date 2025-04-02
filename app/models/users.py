from app.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

class Users(db.Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(256))
    password_salt: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(32))
    address: Mapped[str] = mapped_column(String(100))
    phone_number: Mapped[str] = mapped_column(String(32))