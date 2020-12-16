import requests_cache
from flask import current_app
from pyld import jsonld

from d3api.api.resources.node import NodeById
from d3api.api.views import api, blueprint
from d3api.extensions import apispec

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class FunctionById(NodeById):
    """
    ---
    get:
      tags:
      - functions
      summary: aspect by its uuid
      parameters:
        - in: path
          schema: UuidInputSchema
      responses:
        200:
          content:
            application/json:
              schema: FunctionSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """
    FILTER_ASPECT = 'function'

    # ToDo: update apidoc strings
    # def my_filter_aspect(self):
    #     return Node.aspect == 'function'


class FunctionByIdAndContext(FunctionById):
    """
    ---
    get:
      tags:
      - functions
      summary: aspect by its uuid
      parameters:
        - in: path
          schema: UuidInputSchema
        - in: path2
          schema: UuidInputSchema
      responses:
        200:
          content:
            application/json:
              schema: FunctionSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """
    # ToDo: update apidoc strings


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=FunctionById, app=current_app)
    apispec.spec.path(view=FunctionByIdAndContext, app=current_app)


api.add_resource(FunctionByIdAndContext, '/functions/<uuid:query_id>/<path:context>')
api.add_resource(FunctionById, '/functions/<uuid:query_id>')
