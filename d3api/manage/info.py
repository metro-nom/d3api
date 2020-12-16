from sqlalchemy import func

from d3api.extensions import db
from d3api.manage.cli import cli
from d3api.models import Node


@cli.command("info")
def info():
    """Outputs a data summary"""
    print('info ...')
    query = db.session.query(Node.id)
    cnt_all = query.count()
    print('-' * 80)
    print('sum of all nodes: {}'.format(cnt_all))
    query = db.session.query(Node.json['scope'].astext,
                             func.count(Node.json['scope'].astext)).group_by(
        Node.json['scope'].astext)
    print('-' * 80)
    for (cnt_name, cnt_counter) in query.all():
        if cnt_name is not None:
            print('{:_<74s}{:_>6d}'.format(cnt_name, cnt_counter))
    print('-' * 80)
    return 0
