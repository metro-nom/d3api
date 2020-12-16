import flask

blueprint = flask.Blueprint('error_handlers', __name__)


@blueprint.app_errorhandler(404)
def handle404(e):  # noqa
    return ({'message': "Not found.",
             'status': 404,
             }, 404)
