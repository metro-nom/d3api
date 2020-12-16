import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Base configuration"""
    ENV = os.getenv("FLASK_ENV")
    SECRET_KEY = os.getenv("D3API_SECRET")
    D3URI_API = os.getenv("D3URI_API", default='')
    D3URI_SCHEMA = os.getenv("D3URI_SCHEMA", default='')
    D3URI_SCHEMA_PROD = D3URI_SCHEMA + '/product/'
    D3URI_SCHEMA_FUNC = D3URI_SCHEMA + '/function/'
    D3URI_SCHEMA_LOCT = D3URI_SCHEMA + '/location/'
    D3URI_CONTEXT = os.getenv("D3URI_CONTEXT", default='')


class ProductionConfig(Config):
    """Production configuration"""

    ENV = os.getenv("FLASK_ENV")
    DEBUG = ENV == "development"
    SECRET_KEY = os.getenv("D3API_SECRET")

    SQLALCHEMY_DATABASE_URI = os.getenv("D3API_DB_URI", default='sqlite:///:memory:')
    # SQLALCHEMY_BINDS
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 20

    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    ERROR_404_HELP = False

    # CORS_ENABLED = True

    # SCHEDULER_ALLOWED_HOSTS = ['']
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }
    SCHEDULER_API_ENABLED = False

    JOBS = []


class DevelopmentConfig(Config):
    """Development configuration"""

    SQLALCHEMY_DATABASE_URI = os.getenv("D3API_DB_URI", default='sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 20
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']

    ERROR_404_HELP = False


class TestingConfig(Config):
    """Testing configuration"""

    SQLALCHEMY_DATABASE_URI = os.getenv("D3API_DB_URI", default='sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
