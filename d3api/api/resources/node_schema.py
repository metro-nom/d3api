from marshmallow import Schema, fields

from d3api.extensions import ma
from d3api.models import Node


class NodeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Node
        load_instance = True


class NodeListSchema(Schema):
    items = fields.List(fields.Nested(NodeSchema()))
