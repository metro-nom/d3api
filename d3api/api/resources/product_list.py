import requests_cache
from flask import current_app
from pyld import jsonld

from d3api.api.resources.node_list import NodeList
from d3api.api.views import api, blueprint
from d3api.config import Config
from d3api.extensions import apispec

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class ProductList(NodeList):
    """
    ---
    get:
      tags:
      - products
      summary: all products
      parameters:
        - in: query
          name: start
          schema:
            type: integer
            minimum: 0
          description: start counter for the first result
        - in: query
          name: end
          schema:
            type: integer
            minimum: 0
          description: end counter for the last result
        - in: query
          name: sort
          schema:
            type: string
          description: sort by this field name
        - in: query
          name: order
          schema:
            type: string
            enum:
              - asc
              - desc
          description: asc/desc
      responses:
        200:
          content:
            application/json:
              schema: NodeListSchema
          headers:
            Access-Control-Expose-Headers:
              schema:
                type: string
                example: X-Total-Count
            X-Total-Count:
              schema:
                type: integer
              description: Number of results.
    options:
      tags:
      - products
      parameters:
        - in: query
          name: start
          schema:
            type: integer
            minimum: 0
          description: start counter for the first result
        - in: query
          name: end
          schema:
            type: integer
            minimum: 0
          description: end counter for the last result
        - in: query
          name: sort
          schema:
            type: string
          description: sort by this field name
        - in: query
          name: order
          schema:
            type: string
            enum:
              - asc
              - desc
          description: asc/desc
      responses:
        '204':
          description: get options was successfully.
          headers:
            Access-Control-Expose-Headers:
              schema:
                type: string
                example: X-Total-Count
            X-Total-Count:
              schema:
                type: integer
              description: Number of results.
    """
    FILTER_CONTEXT = Config.D3URI_CONTEXT + "/product.jsonld"


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=ProductList, app=current_app)


api.add_resource(ProductList, '/products')
