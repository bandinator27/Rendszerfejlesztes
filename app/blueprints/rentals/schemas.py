from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List

class RentalsResponseSchema(Schema):
    carid: fields.Integer()
    renterid: fields.Integer()
    rentedat: fields.String()
    rentstatus: fields.String()
    rentduration: fields.Integer()
    rentprice: fields.Integer()
    renteraddress: fields.String()
    renterphonenum: fields.String()