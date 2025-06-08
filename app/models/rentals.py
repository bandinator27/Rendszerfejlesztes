from app.extensions import db
from sqlalchemy import ForeignKey, String, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

class Rentals(db.Model):
    __tablename__ = "Rentals"
    rentalid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    carid: Mapped[int] = mapped_column(ForeignKey("Cars.carid"))
    renterid: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    rentstart: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    rentstatus: Mapped[str] = mapped_column(String(20), nullable=False)
    rentduration: Mapped[int] = mapped_column(Integer, nullable=False)
    rentprice: Mapped[int] = mapped_column(Integer, nullable=False)
    renteraddress: Mapped[str] = mapped_column(String(100), nullable=False)
    renterphonenum: Mapped[str] = mapped_column(String(32), nullable=False)