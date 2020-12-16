import requests_cache
import ttl_cache
from flask import current_app
from pyld import jsonld

from d3api.api.resources.base import D3BaseList
from d3api.api.views import api, blueprint
from d3api.extensions import apispec
from d3api.extensions import db
from d3api.models import Node

jsonld.set_document_loader(jsonld.requests_document_loader(timeout=4))
requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=120)


class TagList(D3BaseList):
    """
    ---
    get:
      tags:
      - aspects
      summary: all aspects
      responses:
        200:
          content:
            application/json:
              schema: AspectListSchema
    """

    @ttl_cache(120.0)  # noqa
    def get_all_tags(self):
        tag_set = set()
        query = db.session.query(Node.json['tags'])
        query = self.filter_aspect(query)
        query = query.filter(Node.json['tags'] is not None)
        for tags in query.all():
            for tag in tags:
                if type(tag) is list:
                    for subtag in tag:
                        tag_set.add(subtag)
                else:
                    tag_set.add(tag)
        return tag_set

    def get(self):
        param_ids = self.get_requested_ids()
        tag_set = self.get_all_tags()
        if param_ids:
            tag_set = tag_set.intersection(set(param_ids))
        json_list = [{'@id': i,
                      'name': i} for i in tag_set]
        return json_list, 200, {'Access-Control-Expose-Headers': 'X-Total-Count',
                                'X-Total-Count': len(json_list),
                                'Cache-Control': 'max-age=300'
                                }

    def post(self):
        return self.get()


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=TagList, app=current_app)


api.add_resource(TagList, '/tags')
