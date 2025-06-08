from marshmallow import Schema, EXCLUDE
from apiflask.fields import String, Integer
from datetime import datetime

class RentalsSchema(Schema):
    rentalid = Integer(required=True)
    carid = Integer()
    renterid = Integer()
    rentstart = String()
    rentstatus = String()
    rentduration = Integer()
    rentprice = Integer()
    renteraddress = String()
    renterphonenum = String()

class RentalRequestSchema(Schema):
    rentstart = String(required=True)
    rentduration = Integer(required=True)

    class Meta:
        unknown = EXCLUDE

    @staticmethod
    def parse_date(date_str):
        return datetime.strptime(date_str, '%Y-%m-%d')