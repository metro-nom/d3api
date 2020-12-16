from marshmallow import Schema, fields

from d3api.extensions import ma
from d3api.models import Node


class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        load_instance = True


class LocationListSchema(Schema):
    items = fields.List(fields.Nested(LocationSchema()))
