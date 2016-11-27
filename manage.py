# coding: utf-8
import logging

from flask.ext.script import Manager

from app import app
from blueprints.models import Person
from blueprints.models import PersonSubscriptions
from blueprints.models import Post
from blueprints.models import Comment
from blueprints.models import Likes
from blueprints.functions import demo_add_comment
from blueprints.functions import demo_add_post
from blueprints.functions import subscribe_on_target_person
from blueprints.functions import demo_random_subs
from blueprints.functions import demo_add_person


logger = logging.getLogger(__name__)
manager = Manager(app)


@manager.command
def init_db():
    for model in [Person, PersonSubscriptions, Post, Comment, Likes]:
        if not model.table_exists():
            model.create_table()
            logger.info(u"Table {} created - OK".format(model.__name__))
        else:
            logger.info(u"Table {} already exists".format(model.__name__))


@manager.command
def clear_db():
    for model in [Person, PersonSubscriptions, Post, Comment, Likes]:
        if model.table_exists():
            model.drop_table()
        model.create_table()
        logger.info(u"Table '{}' re-created - OK".format(model.__name__))


@manager.option("-n", dest="num")
def add_user(num):
    if not num:
        num = 1
    if not isinstance(num, int):
        num = int(num)
    for i in range(num):
        r = demo_add_person()
        while not r:
            r = demo_add_person()
        logger.debug(u"p-{}".format(i))


@manager.option("-o", dest="owner")
@manager.option("-f", dest="follower")
def sub(owner, follower):
    if owner and follower and subscribe_on_target_person(owner_id=owner, follower_id=follower):
        logger.info(u"OK")
    else:
        logger.info(u"Failed")


@manager.option("-n", dest="num")
def rsub(num):
    if not num:
        num = 1
    if not isinstance(num, int):
        num = int(num)
    demo_random_subs(num)


@manager.option("-o", dest="owner")
def add_post(owner):
    if demo_add_post(owner):
        logger.info(u"OK")
    else:
        logger.info(u"Failed")


@manager.option("-a", dest="author_id")
@manager.option("-p", dest="post_id")
@manager.option("-n", dest="num")
def add_comm(author_id, post_id, num):
    if not num:
        num = 1
    if not isinstance(num, int):
        num = int(num)
    for _ in xrange(num):
        if demo_add_comment(author_id, post_id):
            logger.info(u"OK")
        else:
            logger.info(u"Failed")


if __name__ == "__main__":
    manager.run()
