__author__ = 'vladimir'

from flask.ext.script import Manager

from app import app
from blueprints.models import init_database
from blueprints.models import clear_db as recreate_database
from blueprints.security import demo_add_person, demo_random_subs, subscribe_on_target_person
from blueprints.main import demo_add_post, demo_add_comment


manager = Manager(app)


@manager.command
def init_db():
    init_database()


@manager.command
def clear_db():
    recreate_database()


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
        print "p-{0}".format(i)


@manager.option("-o", dest="owner")
@manager.option("-f", dest="follower")
def sub(owner, follower):
    if owner and follower and subscribe_on_target_person(owner_id=owner, follower_id=follower):
        print "OK"
    else:
        print "Fuck"


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
        print "OK"
    else:
        print "Fuck"


@manager.option("-a", dest="author_id")
@manager.option("-p", dest="post_id")
@manager.option("-n", dest="num")
def add_comm(author_id, post_id, num):
    if not num:
        num = 1
    if not isinstance(num, int):
        num = int(num)
    for _ in range(num):
        if demo_add_comment(author_id, post_id):
            print "OK"
        else:
            print "Fuck"


if __name__ == "__main__":
    manager.run()


"""
# register
curl -v -X POST -d 'vkid=3sfddd&recovery_code=12o_pda_iod' http://127.0.0.1:8080/register_user

# register with list of vk-friends
curl -v -X POST -d 'vkid=id0013j&recovery_code=abc-check-reg&fr=id9616&&fr=id7987&fr=id6530' http://127.0.0.1:8080/register_user

# create post
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&food=iiko877&food=iiko653333&text="I like foo"' http://127.0.0.1:8080/create_post

curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&food=iiko1&food=iiko32x&text="I like food, Piter food is cool!!!"' http://127.0.0.1:8080/create_post

# get personal feed
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd

curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd&order=likes

curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/get_feed?vkid=3sfddd&order=date

# like
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&post_id=1' http://127.0.0.1:8080/like_post

# dislike
curl -v -X POST --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd&post_id=3' http://127.0.0.1:8080/dislike_post

# get detailed likes
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' -d 'vkid=3sfddd' http://127.0.0.1:8080/get_likes_to_post?post_id=1

# get global feed
curl -v -X GET --cookie 'auth=wmfe-013443b2-da9b-464c-8e74-dadd1ffef53a' http://127.0.0.1:8080/global_feed?vkid=3sfddd

"""
