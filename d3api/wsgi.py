import os

from d3api.app import create_app

app = create_app(os.environ["FLASK_CONFIG"])
