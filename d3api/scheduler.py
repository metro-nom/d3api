import requests_cache

from d3api.extensions import scheduler

requests_cache.install_cache('jsonld_cache', backend='memory', expire_after=30)


def job0():
    with scheduler.app.app_context():
        print('Job 0 start')
