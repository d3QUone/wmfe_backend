__author__ = 'vladimir'

from flask.ext.script import Manager

from app import app
from blueprints.models import init_database
from blueprints.models import clear_db as recreate_database


manager = Manager(app)


@manager.command
def init_db():
    init_database()


@manager.command
def clear_db():
    recreate_database()


if __name__ == "__main__":
    manager.run()
