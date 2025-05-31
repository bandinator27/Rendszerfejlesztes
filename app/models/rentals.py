from app.database import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String
from sqlalchemy.sql import func
from datetime import datetime

class Rentals(db.Model):
    __tablename__ = "Rentals"
    carid: Mapped[int] = mapped_column(ForeignKey("Cars.carid"), primary_key = True)
    renterid: Mapped[int] = mapped_column(ForeignKey("Users.id"), primary_key = True, nullable=True)
    rentstart: Mapped[datetime] = mapped_column(server_default=func.now())
    rentstatus: Mapped[str] = mapped_column(String(20))
    rentduration: Mapped[int] = mapped_column(String(2))
    rentprice: Mapped[int] = mapped_column(String(5))
    renteraddress: Mapped[str] = mapped_column(String(100))
    renterphonenum: Mapped[str] = mapped_column(String(32))