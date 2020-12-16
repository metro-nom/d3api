import datetime

from flask import current_app
from flask import request
from flask_restful import Resource

from d3api.api.resources.graph_find_svg import get_svg_url
from d3api.api.views import api, blueprint
from d3api.config import Config
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node


class GraphData(Resource):

    def append_node(self, obj_id, ret_dict, recursive_cnt=1):
        if recursive_cnt < 1:
            return
        db_obj = db.session.query(Node).filter(
            Node.context.in_([Config.D3URI_CONTEXT + '/product.jsonld',
                              Config.D3URI_CONTEXT + '/location.jsonld',
                              Config.D3URI_CONTEXT + '/function.jsonld']),
            Node.id == obj_id).first()
        ret_dict['nodes'][db_obj.id] = {
            'id': db_obj.id,
            'label': db_obj.json['name'],
            'svg': get_svg_url(db_obj.json['d3_type']),
        }
        if 'hasPart' in db_obj.json:
            has_part_objs = db.session.query(Node).filter(
                Node.context.in_([Config.D3URI_CONTEXT + '/product.jsonld',
                                  Config.D3URI_CONTEXT + '/location.jsonld',
                                  Config.D3URI_CONTEXT + '/function.jsonld']),
                Node.id.in_(db_obj.json['hasPart'])).all()
            for obj in has_part_objs:
                ret_dict['nodes'][obj.id] = {
                    'id': obj.id,
                    'label': obj.json['name'],
                    'svg': get_svg_url(obj.json['d3_type']),
                }
                ret_dict['links'][db_obj.id + obj.id] = {
                    'source': db_obj.id,
                    'target': obj.id,
                }
                self.append_node(obj.id, ret_dict, recursive_cnt - 2)

        if 'providesFunction' in db_obj.json:
            provides_function_objs = db.session.query(Node). \
                filter_by(context=Config.D3URI_CONTEXT + '/function.jsonld'). \
                filter(Node.id.in_(db_obj.json['providesFunction'])).all()
            for obj in provides_function_objs:
                ret_dict['nodes'][obj.id] = {
                    'id': obj.id,
                    'label': obj.json['name'],
                    'svg': get_svg_url(obj.json['d3_type']),
                }
                ret_dict['links'][db_obj.id + obj.id] = {
                    'label': 'providesFunction',
                    'source': db_obj.id,
                    'target': obj.id,
                }
                self.append_node(obj.id, ret_dict, recursive_cnt - 1)

        if 'containedIn' in db_obj.json:
            contained_in_obj = db.session.query(Node). \
                filter_by(context=Config.D3URI_CONTEXT + '/location.jsonld'). \
                filter(Node.id == db_obj.json['containedIn']).first()
            ret_dict['nodes'][contained_in_obj.id] = {
                'id': contained_in_obj.id,
                'label': contained_in_obj.json['name'],
                'svg': get_svg_url(contained_in_obj.json['d3_type']),
            }
            ret_dict['links'][db_obj.id + contained_in_obj.id] = {
                'label': 'containedIn',
                'source': db_obj.id,
                'target': contained_in_obj.id,
            }
            self.append_node(contained_in_obj.id, ret_dict, recursive_cnt - 1)

        if 'isPartOf' in db_obj.json:
            is_part_of_obj = db.session.query(Node).filter(
                Node.context.in_([Config.D3URI_CONTEXT + '/product.jsonld',
                                  Config.D3URI_CONTEXT + '/location.jsonld',
                                  Config.D3URI_CONTEXT + '/function.jsonld']),
                Node.id == db_obj.json['isPartOf']).first()
            ret_dict['nodes'][is_part_of_obj.id] = {
                'id': is_part_of_obj.id,
                'label': is_part_of_obj.json['name'],
                'svg': get_svg_url(is_part_of_obj.json['d3_type']),
            }
            ret_dict['links'][(db_obj.id + is_part_of_obj.id)] = {
                'label': 'isPartOf',
                'source': db_obj.id,
                'target': is_part_of_obj.id,
            }
            self.append_node(is_part_of_obj.id, ret_dict, recursive_cnt - 3)

        if 'containsProduct' in db_obj.json:
            contains_product_objs = db.session.query(Node). \
                filter_by(context=Config.D3URI_CONTEXT + '/location.jsonld'). \
                filter(Node.id.in_(db_obj.json['containsProduct'])).all()
            for obj in contains_product_objs:
                ret_dict['nodes'][obj.id] = {
                    'id': obj.id,
                    'label': obj.json['name'],
                    'svg': get_svg_url(obj.json['d3_type']),
                }
                ret_dict['links'][db_obj.id + obj.id] = {
                    'label': 'containsProduct',
                    'source': db_obj.id,
                    'target': obj.id,
                }
                self.append_node(obj.id, ret_dict, recursive_cnt - 1)

        if 'usesFunction' in db_obj.json:
            uses_function_objs = db.session.query(Node). \
                filter_by(context=Config.D3URI_CONTEXT + '/product.jsonld'). \
                filter(Node.id.in_(db_obj.json['usesFunction'])).all()
            for obj in uses_function_objs:
                ret_dict['nodes'][obj.id] = {
                    'id': obj.id,
                    'label': obj.json['name'],
                    'svg': get_svg_url(obj.json['d3_type']),
                }
                ret_dict['links'][db_obj.id + obj.id] = {
                    'label': 'usesFunction',
                    'source': db_obj.id,
                    'target': obj.id,
                }
                self.append_node(obj.id, ret_dict, recursive_cnt - 1)

    def get(self):
        t_start = datetime.datetime.now()
        work_dict = {'nodes': {},
                     'links': {}}
        param_id = request.args.get('id')
        if param_id is None:
            work_dict = {'nodes': [{'id': "_"}], 'links': []}
            return work_dict, 200
        self.append_node(param_id, work_dict, recursive_cnt=3)
        ret_dict = {
            'nodes': list(work_dict['nodes'].values()),
            'links': list(work_dict['links'].values())
        }
        t_delta = int((datetime.datetime.now() - t_start).total_seconds() * 1000)
        return ret_dict, 200, {
            'Access-Control-Expose-Headers': 'X-Total-Count',
            'X-Perf-MSec': t_delta,
        }


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=GraphData, app=current_app)


api.add_resource(GraphData, '/graph_data')
