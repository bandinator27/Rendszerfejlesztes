from app.database import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import String

class Cars(db.Model):
    __tablename__ = "Cars"
    carid: Mapped[int] = mapped_column(primary_key = True)
    numberplate: Mapped[str] = mapped_column(String(32))
    rentable: Mapped[int]
    price: Mapped[int]
    manufacturer: Mapped[str] = mapped_column(String(32))
    model: Mapped[str] = mapped_column(String(32))
    color: Mapped[str] = mapped_column(String(32))
    seats: Mapped[int]
    interior: Mapped[str] = mapped_column(String(32))
    bodytype: Mapped[str] = mapped_column(String(32))
    gearbox: Mapped[str] = mapped_column(String(32))
    doors: Mapped[int]
    fueltype: Mapped[str] = mapped_column(String(32))
    topspeed: Mapped[int]
    power: Mapped[int]
    kmcount: Mapped[int]
    enginetype: Mapped[str] = mapped_column(String(32))
    extras: Mapped[str] = mapped_column(String(100))