import click
from flask.cli import FlaskGroup

from d3api.app import create_app
from d3api.extensions import db


# noinspection PyUnusedLocal
def create_d3api(info):
    return create_app(config_name=None)


@click.group(cls=FlaskGroup, create_app=create_d3api)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables
    and create a new user named admin with password admin
    """
    click.echo("create database")
    db.create_all()
    click.echo("done")
    db.session.commit()
