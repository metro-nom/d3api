from marshmallow import Schema, fields

from d3api.extensions import ma
from d3api.models import Node


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        load_instance = True


class ProductListSchema(Schema):
    items = fields.List(fields.Nested(ProductSchema()))
