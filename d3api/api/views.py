from flask import Blueprint
from flask_restful import Api

from d3api.api.errors import custom_errors

blueprint = Blueprint('api', __name__, url_prefix='')
api = Api(blueprint, errors=custom_errors)
