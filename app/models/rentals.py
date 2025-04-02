from app.database import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String
from sqlalchemy import ForeignKey
from sqlalchemy.sql.functions import now
from datetime import datetime

class Rentals(db.Model):
    __tablename__ = "Rentals"
    carid: Mapped[int] = mapped_column(ForeignKey("Cars.carid"), primary_key = True)
    renterid: Mapped[int] = mapped_column(ForeignKey("Users.id"), primary_key = True)
    rentedat: Mapped[datetime] = mapped_column(server_default=now())
    rentstatus: Mapped[str] = mapped_column(String(20))
    rentduration: Mapped[int]
    rentprice: Mapped[int]
    renteraddress: Mapped[str] = mapped_column(String(100))
    renterphonenum: Mapped[str] = mapped_column(String(32))