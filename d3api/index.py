from flask import Blueprint, redirect

index_blueprint = Blueprint('index', __name__)


@index_blueprint.route("/")
def index():
    return redirect("/swagger-ui#/", code=302)
