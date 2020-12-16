from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('meta', __name__, url_prefix='/meta')
api = Api(blueprint)
