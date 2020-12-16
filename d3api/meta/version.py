import pkg_resources
from flask import current_app
from flask_restful import Resource
from marshmallow import Schema, fields

from d3api.extensions import apispec
from d3api.meta.views import api, blueprint


class VersionSchema(Schema):
    name = fields.Str(required=True)
    version = fields.Str(required=True)


version = pkg_resources.require("d3api")[0].version


class Version(Resource):
    """Single object resource

    ---
    get:
      tags:
        - meta
      responses:
        200:
          content:
            application/json:
                schema: VersionSchema
    """

    @staticmethod
    def get():
        return {'name': 'd3api',
                'version': version}


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=Version, app=current_app)


api.add_resource(Version, '/version')
