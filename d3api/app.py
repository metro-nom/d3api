from flask import Flask
from flask_cors import CORS

from d3api import api, meta
from d3api.extensions import db, ma, jwt, apispec, scheduler
from .error_handlers import blueprint as error_blueprint
from .index import index_blueprint


def create_app(config_name):
    """Application factory, used to create application
    """
    app = Flask('d3api')
    config_module = f"d3api.config.{config_name.capitalize()}Config"
    app.config.from_object(config_module)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    CORS(app, resources=r'/*')
    return app


def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    # start_datetime = datetime.now() + timedelta(seconds=10)
    # scheduler.add_job(id='job0', func=job0, run_date=start_datetime)
    # if cli is True:
    #     migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    apispec.init_app(app)
    apispec.spec.components.security_scheme("jwt", {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    })
    apispec.spec.components.schema(
        "PaginatedResult", {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }})


def configure_graphdb(app):
    app.nx_cache = None
    app.graphdb = {'val': 1}


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(api.views.blueprint)
    app.register_blueprint(meta.views.blueprint)
    app.register_blueprint(error_blueprint)
    app.register_blueprint(index_blueprint)
