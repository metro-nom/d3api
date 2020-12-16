import requests_cache
from flask import current_app
from pyld import jsonld

from d3api.api.resources.node import NodeById
from d3api.api.views import api, blueprint
from d3api.extensions import apispec

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class ProductById(NodeById):
    """
    ---
    get:
      tags:
      - products
      summary: aspect by its uuid
      parameters:
        - in: path
          schema: UuidInputSchema
      responses:
        200:
          content:
            application/json:
              schema: ProductSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """
    FILTER_ASPECT = 'product'

    # ToDo: update apidoc strings


class ProductByIdAndContext(ProductById):
    """
    ---
    get:
      tags:
      - products
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
              schema: ProductSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """
    # ToDo: update apidoc strings


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=ProductById, app=current_app)


api.add_resource(ProductByIdAndContext, '/products/<uuid:query_id>/<path:context>')
api.add_resource(ProductById, '/products/<uuid:query_id>')
