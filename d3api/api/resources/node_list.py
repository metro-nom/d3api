import requests_cache
import ttl_cache
from flask import current_app, request
from pyld import jsonld
from sqlalchemy import Unicode
from sqlalchemy import cast, JSON

from d3api.api.resources.base import D3BaseList
from d3api.api.resources.node import my_expand_compact
from d3api.api.views import api, blueprint
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class NodeList(D3BaseList):
    """
    ---
    get:
      tags:
      - nodes
      summary: all nodes
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
      - nodes
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
    FILTER_CONTEXT = None

    def filter_search2(self, query):
        param_query = request.args.get('query')
        if param_query is not None:
            query = query.filter(Node.json.cast(Unicode).contains(param_query))
        return query

    @staticmethod
    def filter_search(query):
        param_query = request.args.get('query')
        if param_query is not None:
            sq1 = db.session.query(Node.id). \
                filter(Node.json.cast(Unicode).contains(param_query)). \
                group_by(Node.id). \
                subquery()
            node_q1 = query
            node_q2 = node_q1.join(sq1, sq1.c.id == Node.id)
            return node_q2
        else:
            return query

    def filter_my_aspect(self, query):
        if self.FILTER_CONTEXT is not None:
            query = query.filter(
                Node.json['aspect'] == cast(self.FILTER_CONTEXT, JSON))
        return query

    @ttl_cache(120.0)  # noqa
    def get(self):
        query = db.session.query(Node.id, Node.json, Node.expanded)
        query = self.filter_id(query)
        query = self.filter_context(query)
        # query = self.filter_my_aspect(query)
        query = self.filter_d3_type(query)
        query = self.filter_scope(query)
        query = self.filter_aspect(query)
        query = self.filter_report_vm_os(query)
        query = self.filter_report_power_state(query)
        query = self.filter_ip(query)
        query = self.filter_fqdn(query)
        query = self.filter_search(query)
        total_cnt = len(self.get_requested_ids())
        query = self.filter_sorter(query)
        query = self.filter_paginate(query)
        if total_cnt == 0:
            total_cnt = query.total
        ret_list, ret_len = my_expand_compact(query.items)
        return ret_list, 200, {'Access-Control-Expose-Headers': 'X-Total-Count',
                               'X-Total-Count': total_cnt,
                               'Cache-Control': 'max-age=300'
                               }

    @ttl_cache(120.0)  # noqa
    def post(self):
        return self.get()

    @ttl_cache(120.0)  # noqa
    def options(self):
        query = db.session.query(Node)
        query = self.filter_id(query)
        query = self.filter_aspect(query)
        query = self.filter_search(query)
        total_cnt = query.count()
        return None, 204, {'Access-Control-Expose-Headers': 'X-Total-Count',
                           'X-Total-Count': total_cnt,
                           'Cache-Control': 'max-age=300'
                           }


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=NodeList, app=current_app)


api.add_resource(NodeList, '/nodes')
