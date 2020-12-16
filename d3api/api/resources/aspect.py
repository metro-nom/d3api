from flask import current_app
from flask_restful import Resource
from marshmallow import Schema, fields

from d3api.api.errors import AspectNotFoundError
from d3api.api.views import api, blueprint
from d3api.extensions import apispec
from d3api.extensions import ma

ASPECTS = [
    {'uuid': '6e493c64-d250-4b1f-af9b-045f4dce9726',
     '@obj_id': 'location',
     'name': 'location',
     'summary': 'summary....',
     'description': 'description....',
     },
    {'uuid': 'decd163c-ca0f-485c-bd9a-fd6b9b9aa4d8',
     '@obj_id': 'function',
     'name': 'function',
     'summary': 'summary....',
     'description': 'description....',
     },
    {'uuid': '14ce1ee8-f4aa-42f1-85a4-df4d156f9029',
     '@obj_id': 'product',
     'name': 'product',
     'summary': 'summary....',
     'description': 'description....',
     }
]


class AspectSchema(Schema):
    id = fields.UUID()
    name = fields.Str(required=True)
    summary = fields.Str(required=True)
    description = fields.Str()
    links = ma.Hyperlinks(
        {"self": ma.URLFor("http://www.essen.de")}
    )


class NameInputSchema(Schema):
    name = fields.Str()


class UuidInputSchema(Schema):
    id = fields.UUID()


class ErrorSchema(Schema):
    message = fields.Str(required=True)
    status = fields.Integer(required=True)


class AspectListSchema(Schema):
    items = fields.List(fields.Nested(AspectSchema()))


class AspectById(Resource):
    """
    ---
    get:
      tags:
      - aspects
      summary: aspect by its uuid
      parameters:
        - in: path
          schema: UuidInputSchema
      responses:
        200:
          content:
            application/json:
              schema: AspectSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """

    @staticmethod
    def get(obj_id):
        my_list = [obj_dict for obj_dict in ASPECTS if obj_dict['obj_id'] == str(obj_id)]
        if len(my_list) == 1:
            return my_list[0]
        else:
            raise AspectNotFoundError()


class AspectByName(Resource):
    """
    ---
    get:
      tags:
      - aspects
      summary: aspect by its name
      parameters:
        - in: path
          schema: NameInputSchema
      responses:
        200:
          content:
            application/json:
              schema: AspectSchema
        404:
          content:
            application/json:
              {
                "message": "Aspect not found.",
                "status": 404
              }
    """

    @staticmethod
    def get(name):
        my_list = [obj_dict for obj_dict in ASPECTS if obj_dict['name'] == name]
        if len(my_list) == 1:
            return my_list[0]
        else:
            raise AspectNotFoundError


class AspectList(Resource):
    """
    ---
    get:
      tags:
      - aspects
      summary: all aspects
      responses:
        200:
          content:
            application/json:
              schema: AspectListSchema
    """

    @staticmethod
    def get():
        return ASPECTS, 200, {'Access-Control-Expose-Headers': 'X-Total-Count',
                              'X-Total-Count': len(ASPECTS),
                              'Cache-Control': 'max-age=300'
                              }


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=AspectById, app=current_app)
    apispec.spec.path(view=AspectByName, app=current_app)
    apispec.spec.path(view=AspectList, app=current_app)


api.add_resource(AspectList, '/aspects')
api.add_resource(AspectById, '/aspects/uuid/<uuid:obj_id>')
api.add_resource(AspectByName, '/aspects/name/<string:name>')
