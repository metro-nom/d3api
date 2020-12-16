import datetime

import requests_cache
from flask import current_app
from flask import request
from flask_restful import Resource
from pyld import jsonld
from sqlalchemy import cast, JSON

from d3api.api.views import api, blueprint
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node

requests_cache.install_cache('jsonld_cache',
                             backend='memory',
                             expire_after=240)
jsonld.set_document_loader(jsonld.requests_document_loader(timeout=30))


# noinspection PyUnresolvedReferences
class NodeExport(Resource):

    @staticmethod
    def expanded_list(query):
        expanded_list = {(i.id, i.context): i.expanded for i in query}
        time_st_1 = datetime.datetime.now()
        ret_dict = {}
        for (obj_id, context), obj_dict in expanded_list.items():
            if obj_id not in ret_dict:
                ret_dict[obj_id] = {}
            ret_dict[obj_id].update(obj_dict)
            # ret_dict[id].update(obj_dict[0])
        return list(ret_dict.values()), len(ret_dict), time_st_1

    def get(self):
        t_start = datetime.datetime.now()
        args_dict = {arg_key: arg_val
                     for arg_key, arg_val
                     in request.args.items()
                     if arg_key not in ['compact']}
        compact = request.args.get('compact')
        # Subselect for selected Node-IDs
        node_ids = db.session.query(Node.id)
        t_delta1 = int((datetime.datetime.now() - t_start).total_seconds() * 1000)
        for arg_key, arg_val in args_dict.items():
            filter_it = Node.json[arg_key] == cast(arg_val, JSON)
            node_ids = node_ids.filter(filter_it)
        node_ids = node_ids.group_by(Node.id).subquery()
        # Main select for all Nodes with the IDs from the subselect
        query = Node.query.join(
            node_ids, Node.id == node_ids.c.id
        )
        t_delta2 = int((datetime.datetime.now() - t_start).total_seconds() * 1000)
        expanded_list, expanded_len, tst_3 = self.expanded_list(query)
        t_delta3 = int((tst_3 - t_start).total_seconds() * 1000)
        t_delta4 = int((datetime.datetime.now() - t_start).total_seconds() * 1000)
        if compact is None:
            return expanded_list, 200, {
                'Access-Control-Expose-Headers': 'X-Total-Count',
                'X-Total-Count': expanded_len,
                'X-Perf-1-MSec': t_delta1,
                'X-Perf-2-MSec': t_delta2,
                'X-Perf-3-MSec': t_delta3,
                'X-Perf-4-MSec': t_delta4,
            }
        else:
            return_list = []
            jsonld_proc = jsonld.JsonLdProcessor()
            for expanded_node in expanded_list:
                compacted_node = jsonld_proc.compact(expanded_node, compact, options=None)
                return_list.append(compacted_node)
            t_delta5 = int((datetime.datetime.now() - t_start).total_seconds() * 1000)
            return return_list, 200, {
                'Access-Control-Expose-Headers': 'X-Total-Count',
                'X-Total-Count': len(return_list),
                'X-Perf-1-MSec': t_delta1,
                'X-Perf-2-MSec': t_delta2,
                'X-Perf-3-MSec': t_delta3,
                'X-Perf-4-MSec': t_delta4,
                'X-Perf-5-MSec': t_delta5,
            }


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=NodeExport, app=current_app)


api.add_resource(NodeExport, '/export')
