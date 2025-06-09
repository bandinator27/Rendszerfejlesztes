from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import ForeignKey

class Users(db.Model):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    password: Mapped[str] = mapped_column(String(32))
    password_salt: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(32))
    address_id: Mapped[int] = mapped_column(ForeignKey("Addresses.id"))
    address = relationship("Addresses", backref="users")
    phone_number: Mapped[str] = mapped_column(String(32))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)