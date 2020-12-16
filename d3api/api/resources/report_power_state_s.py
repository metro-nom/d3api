import requests_cache
import ttl_cache
from flask import current_app
from pyld import jsonld
from sqlalchemy import asc

from d3api.api.resources.base import D3BaseList
from d3api.api.views import api, blueprint
from d3api.config import Config
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class ReportPowerState(D3BaseList):
    """
    ---
    get:
      tags:
      - aspects
      summary: all vm guest operating systems
      responses:
        200:
          content:
            application/json:
              schema: AspectListSchema
    """

    @ttl_cache(60.0)  # noqa
    def get(self):
        query = db.session.query(Node.json['power_state'].astext)
        query = self.filter_aspect(query)
        query = query.filter(Node.context == Config.D3URI_CONTEXT + "/vmware_vm.jsonld")
        query = query.group_by(Node.json['power_state'].astext)
        query = query.order_by(asc(Node.json['power_state'].astext))
        total_cnt = query.count()
        json_list = [{'@id': i[0],
                      'name': i[0]} for i in query.all()]
        return json_list, 200, {'Access-Control-Expose-Headers': 'X-Total-Count',
                                'X-Total-Count': total_cnt,
                                'Cache-Control': 'max-age=300'
                                }


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=ReportPowerState, app=current_app)


api.add_resource(ReportPowerState, '/report_power_state')
