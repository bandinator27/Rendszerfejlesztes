from marshmallow import Schema, fields
from apiflask.fields import String, Email, Nested, Integer, List
from apiflask.validators import Email

class AddressSchema(Schema):
    city = fields.String()
    street = fields.String()
    postalcode = fields.Integer()

class RoleSchema(Schema):
    id = fields.Integer()
    role_name = fields.String()

class UserRequestSchema(Schema):
    username = fields.String()
    email = String(validate=Email())
    password = fields.String()
    phone_number = fields.String()
    address = fields.Nested(AddressSchema)

class UserResponseSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    address = fields.Nested(AddressSchema)
    token = fields.String()

class UserLoginSchema(Schema):
    email = String(validate=Email())
    password = fields.String()

class PayloadSchema(Schema):
    user_id = fields.Integer()
    roles = fields.String()
    exp = fields.Integer()