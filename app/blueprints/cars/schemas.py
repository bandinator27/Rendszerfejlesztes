from marshmallow import Schema, fields

class CarsSchema(Schema):
    carid = fields.Integer(dump_only=True)
    numberplate = fields.String()
    rentable = fields.Integer()
    price = fields.Integer()
    manufacturer = fields.String()
    model = fields.String()
    year = fields.Integer()
    color = fields.String()
    seats = fields.Integer()
    interior = fields.String()
    bodytype = fields.String()
    gearbox = fields.String()
    doors = fields.Integer()
    fueltype = fields.String()
    topspeed = fields.Integer()
    power = fields.Integer()
    kmcount = fields.Integer()
    enginetype = fields.String()
    extras = fields.String()
    image_url = fields.String()

class CarsFilterSchema(Schema):
    filter_type = fields.String()
    filterValue = fields.String()