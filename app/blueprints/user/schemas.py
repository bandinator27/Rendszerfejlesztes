from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email

class AddressSchema(Schema):
    city = fields.String()
    street = fields.String()
    postalcode = fields.Integer()

class UserRequestSchema(Schema):
    username = fields.String()
    email = String(validate=Email())
    password = fields.String()
    phonenumber = fields.String()
    address = fields.String()

class UserResponseSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    address = fields.Nested(AddressSchema)

class UserLoginSchema(Schema):
    email = String(validate=Email())
    password = fields.String()