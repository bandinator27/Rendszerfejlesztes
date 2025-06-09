from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

class Addresses(db.Model):
    __tablename__ = "Addresses"
    id: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str] = mapped_column(String(32))
    street: Mapped[str] = mapped_column(String(256))
    postalcode: Mapped[int]