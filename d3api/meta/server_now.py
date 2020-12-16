from datetime import datetime

from flask import current_app
from flask_restful import Resource
from marshmallow import Schema, fields
from pytz import timezone

from d3api.extensions import apispec
from d3api.meta.views import api, blueprint


class NowSchema(Schema):
    now = fields.DateTime(required=True, format='iso')


class ServerNow(Resource):
    """
    ---
    get:
      tags:
        - meta
      responses:
        200:
          content:
            application/json:
                schema: NowSchema
    """

    @staticmethod
    def get():
        berlin = timezone('Europe/Berlin')
        return {'now': datetime.now(berlin).isoformat()}


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=ServerNow, app=current_app)


api.add_resource(ServerNow, '/now')
