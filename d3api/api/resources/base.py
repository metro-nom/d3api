from flask import request
from flask_restful import Resource
from sqlalchemy import Unicode
from sqlalchemy import asc, desc, cast, JSON, func, or_

from d3api.config import Config
from d3api.extensions import db
from d3api.models import Node


class D3BaseList(Resource):
    FILTER_CONTEXT = None

    @staticmethod
    def get_requested_ids():
        json_data = request.json
        if json_data is not None \
                and 'id' in json_data \
                and len(json_data['id']) > 0:
            return json_data['id']
        param_ids = request.args.getlist('id')
        if param_ids is not None \
                and len(param_ids) > 0:
            return param_ids
        return []

    @staticmethod
    def filter_sorter(query):
        param_sort = request.args.get('sort')
        param_order = request.args.get('order')
        if param_order is not None \
                and param_sort is not None:
            if param_order.lower() == "asc":
                query = query.order_by(
                    asc(Node.json[param_sort].astext))
            elif param_order.lower() == "desc":
                query = query.order_by(
                    desc(Node.json[param_sort].astext))
        return query

    @staticmethod
    def filter_paginate(query):
        param_start = request.args.get('start')
        param_end = request.args.get('end')
        if param_start is not None \
                and param_end is not None:
            page_size = int(param_end) - int(param_start)
            first_page = int(param_start) / page_size + 1
            return query.paginate(page=first_page, per_page=page_size)
        return query.paginate()

    def filter_id(self, query):
        param_ids = self.get_requested_ids()
        # param_id = request.args.get('id')
        if param_ids is not None \
                and len(param_ids) > 0:
            # filter_it = Node.id == param_id
            filter_it = Node.id.in_(param_ids)
        else:
            # filter_it = Node.context.contains('base.jsonld')
            if self.FILTER_CONTEXT:
                filter_it = Node.context == self.FILTER_CONTEXT
            else:
                filter_it = Node.context == Config.D3URI_CONTEXT + "/base.jsonld"
        query = query.filter(filter_it)
        return query

    def filter_search2(self, query):
        param_query = request.args.get('query')
        if param_query is not None:
            sq1 = db.session.query(Node.id). \
                filter(Node.json['long_desc'] == cast(param_query, JSON)). \
                group_by(Node.id). \
                subquery()
            node_q1 = query
            node_q2 = node_q1.join(sq1, sq1.c.id == Node.id)
            # node_q3 = node_q2.filter(Node.context.contains('base.jsonld'))
            return node_q2
        else:
            return query

    @staticmethod
    def filter_d3_type(query):
        param_d3_type_id = request.args.get('d3_type_id')
        if param_d3_type_id is not None:
            query = query.filter(
                Node.json['d3_type'] == cast(param_d3_type_id, JSON))
        return query

    @staticmethod
    def filter_report_vm_os(query):
        param_report_vm_os_id = request.args.get('report_vm_os_id')
        if param_report_vm_os_id is not None:
            id_list = db.session.query(Node.id). \
                filter(or_(Node.context == Config.D3URI_CONTEXT + "/vmware_vm.jsonld",
                           Node.context == Config.D3URI_CONTEXT + "/cps_linux.jsonld")). \
                filter(Node.json['guest_os'] == cast(param_report_vm_os_id, JSON)). \
                subquery()
            query = query.filter(
                Node.id.in_(id_list))
        return query

    @staticmethod
    def filter_report_power_state(query):
        param_report_power_state_id = request.args.get('report_power_state_id')
        if param_report_power_state_id is not None:
            id_list = db.session.query(Node.id). \
                filter(Node.context == Config.D3URI_CONTEXT + "/vmware_vm.jsonld"). \
                filter(Node.json['power_state'] == cast(param_report_power_state_id, JSON)). \
                subquery()
            query = query.filter(
                Node.id.in_(id_list))
        return query

    @staticmethod
    def filter_ip(query):
        param_query_ip = request.args.get('query_ip')
        if param_query_ip is not None:
            id_list = db.session.query(Node.id). \
                filter(Node.context == Config.D3URI_CONTEXT + "/vmware_vm.jsonld"). \
                filter(Node.json['guest_ip'] == cast(param_query_ip, JSON)). \
                subquery()
            # id_list = db.session.query(Node.id). \
            #     filter(func.lower(Node.json['guest_ip'].astext) == func.lower(param_query_ip)). \
            #     subquery()
            query = query.filter(
                Node.id.in_(id_list))
        return query

    @staticmethod
    def filter_fqdn(query):
        param_query_fqdn = request.args.get('query_fqdn')
        if param_query_fqdn is not None:
            id_list = db.session.query(Node.id). \
                filter(func.lower(Node.json['host_fqdn'].astext) == func.lower(param_query_fqdn)). \
                subquery()
            query = query.filter(
                Node.id.in_(id_list))
        return query

    @staticmethod
    def filter_scope(query):
        param_scope_id = request.args.get('scope_id')
        if param_scope_id is not None:
            query = query.filter(
                Node.json['scope'] == cast(param_scope_id, JSON))
        return query

    @staticmethod
    def filter_context(query):
        param_context = request.args.get('context')
        if param_context is not None:
            query = query.filter(
                Node.context == param_context)
        return query

    @staticmethod
    def filter_aspect(query):
        param_aspect_id = request.args.get('aspect_id')
        if param_aspect_id is not None:
            query = query.filter(
                Node.json['aspect'] == cast(param_aspect_id, JSON))
        return query

    @staticmethod
    def filter_tags(query):
        param_tag_id = request.args.get('tag_id')
        if param_tag_id is not None:
            query = query.filter(
                Node.json.op('->>')('tags').cast(Unicode).contains(param_tag_id)
            )
        return query
