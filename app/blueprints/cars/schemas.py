from marshmallow import Schema, fields
from apiflask.fields import String, Integer

class CarsResponseSchema(Schema):
    carid: fields.Integer()
    numberplate: fields.String()
    rentable: fields.Integer()
    price: fields.Integer()
    manufacturer: fields.String()
    model: fields.String()
    color: fields.String()
    seats: fields.Integer()
    pictures: fields.String()
    interior: fields.String()
    bodytype: fields.String()
    gearbox: fields.String()
    doors: fields.Integer()
    fueltype: fields.String()
    topspeed: fields.Integer()
    power: fields.Integer()
    torque: fields.Integer()
    enginetype: fields.String()
    extras: fields.String()