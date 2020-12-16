"""Extensions registry

All extensions here are used as singletons and
initialized in application factory
"""
from flask_apscheduler import APScheduler
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

from d3api.commons.apispec import APISpecExt

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
migrate = Migrate()
apispec = APISpecExt()
scheduler = APScheduler()

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')
