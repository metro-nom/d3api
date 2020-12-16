import requests_cache
from flask import current_app, request
from flask_restful import Resource, abort
from pyld import jsonld

from d3api.api.views import api, blueprint
from d3api.config import Config
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


def my_expand_compact(query_in):
    expand = request.args.get('expand')
    compact = request.args.get('compact')
    if expand and expand.lower() == 'true':
        ret_list = [i.expanded for i in query_in]
        ret_len = len(ret_list)
    elif compact is not None:
        ret_dict = {}
        for obj in query_in:
            if obj.id not in ret_dict:
                ret_dict[obj.id] = {}
            ret_dict[obj.id].update(obj.expanded)
        ret_list = []
        jsonld_proc = jsonld.JsonLdProcessor()
        for expanded_node in ret_dict.values():
            compacted_node = jsonld_proc.compact(expanded_node, compact, options=None)
            ret_list.append(compacted_node)
        ret_len = len(ret_list)
    else:
        ret_list = [i.json for i in query_in]
        ret_len = len(ret_list)
    return ret_list, ret_len


class NodeById(Resource):
    """
    ---
    get:
      tags:
      - nodes
      summary: aspect by its uuid
      parameters:
        - in: path
          schema: UuidInputSchema
      responses:
        200:
          content:
            application/json:
              schema: NodeSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """

    def my_filter_aspect(self):
        return Node.aspect == self.FILTER_ASPECT

    def my_query(self, query_id, context=None):
        str_id = '{}/{}s/{}'.format(Config.D3URI_API, self.FILTER_ASPECT, query_id)
        search_query = db.session.query(Node). \
            filter(self.my_filter_aspect()). \
            filter(Node.id == str_id)
        if context is not None:
            search_query = search_query. \
                filter(Node.context == context)
        return search_query.all()

    def get(self, query_id, context=None):
        search_query = self.my_query(query_id, context)
        ret_list, ret_len = my_expand_compact(search_query)
        if ret_len < 1:
            abort(404, message="query_id '{}' doesn't exist".format(query_id))
        if ret_len == 1:
            return ret_list[0], 200, {
                'Access-Control-Expose-Headers': 'X-Total-Count',
                'X-Total-Count': 1,
                'Cache-Control': 'max-age=300'
            }
        else:
            return ret_list, 200, {
                'Access-Control-Expose-Headers': 'X-Total-Count',
                'X-Total-Count': ret_len,
                'Cache-Control': 'max-age=300'
            }

    def options(self, query_id, context=None):
        result_json = self.get(query_id, context)
        return None, 204, {'Access-Control-Expose-Headers': 'X-Total-Count',
                           'X-Total-Count': len(result_json),
                           'Cache-Control': 'max-age=300'
                           }


class NodeByIdAndContext(NodeById):
    """
    ---
    get:
      tags:
      - nodes
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
              schema: NodeSchema
        404:
          content:
            application/json:
              schema: ErrorSchema
    """
    FILTER_ASPECT = 'node'


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=NodeById, app=current_app)
    apispec.spec.path(view=NodeByIdAndContext, app=current_app)


api.add_resource(NodeByIdAndContext, '/nodes/<uuid:query_id>/<path:context>')
api.add_resource(NodeById, '/nodes/<uuid:query_id>')
