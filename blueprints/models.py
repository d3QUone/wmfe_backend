__author__ = 'vladimir'

import datetime

from flask_peewee import db
from flask_peewee.db import DoesNotExist


database = db.MySQLDatabase('wmfe_backend', **{'host': '127.0.0.1', 'password': 'MuchSecurePassword', 'user': 'vladimir'})


class BaseModel(db.Model):
    class Meta:
        database = database


class Person(BaseModel):
    vkid = db.CharField(unique=True, primary_key=True)
    auth_cookie = db.CharField()
    auth_token = db.CharField()
    recovery_code = db.CharField()
    my_followers = db.IntegerField(default=0)
    following = db.IntegerField(default=0)
    posts = db.IntegerField(default=0)


class PersonSubscriptions(BaseModel):
    owner = db.ForeignKeyField(Person, related_name="main", on_delete="CASCADE", on_update="CASCADE")
    follower = db.ForeignKeyField(Person, related_name="my_follower", on_delete="CASCADE", on_update="CASCADE")


class Post(BaseModel):
    post_id = db.PrimaryKeyField()
    author = db.ForeignKeyField(Person, related_name="Post", on_delete="CASCADE", on_update="CASCADE")
    text = db.TextField()
    pic_url = db.CharField()
    date = db.DateTimeField(default=datetime.datetime.now)
    latitude = db.DecimalField(max_digits=10, decimal_places=6, auto_round=False)  # -90; 90
    longitude = db.DecimalField(max_digits=10, decimal_places=6, auto_round=False)  # -180; 180
    likes = db.IntegerField(default=0)
    comments = db.IntegerField(default=0)
    is_deleted = db.BooleanField(default=False)


class Comment(BaseModel):
    post = db.ForeignKeyField(Post, related_name="Comment", on_delete="CASCADE", on_update="CASCADE")
    author = db.ForeignKeyField(Person, related_name="Comment", on_delete="CASCADE", on_update="CASCADE")
    text = db.TextField()
    date = db.DateTimeField(default=datetime.datetime.now)
    is_deleted = db.BooleanField(default=False)


class Likes(BaseModel):
    person = db.ForeignKeyField(Person, related_name="Likes", on_delete="CASCADE", on_update="CASCADE")
    post = db.ForeignKeyField(Post, related_name="Likes", on_delete="CASCADE", on_update="CASCADE")
    is_deleted = db.BooleanField(default=False)


GEO_DIST_PRC = """
delimiter $$
CREATE PROCEDURE geodist (IN mylon DECIMAL, IN mylat DECIMAL, IN dist INT)
BEGIN
    declare lon1 float;
    declare lat1 float;

    declare lon2 float;
    declare lat2 float;

    -- calculate lon and lat for the rectangle:
    set lon1 = mylon-dist/abs(cos(radians(mylat))*69);
    set lon2 = mylon+dist/abs(cos(radians(mylat))*69);
    set lat1 = mylat-(dist/69);
    set lat2 = mylat+(dist/69);

    -- run the query:
    SELECT destination.*,3956 * 2 * ASIN(SQRT( POWER(SIN((orig.lat -dest.lat) * pi()/180 / 2), 2) +COS(orig.lat * pi()/180) * COS(dest.lat * pi()/180) *POWER(SIN((orig.lon -dest.lon) * pi()/180 / 2), 2) )) as distance FROM users destination, users origin
    WHERE origin.id=userid AND destination.longitude between lon1 AND lon2 AND destination.latitude between lat1 AND lat2
    HAVING distance < dist ORDER BY Distance LIMIT 10;
END $$
delimiter ;
"""


def init_database():
    for model in [Person, PersonSubscriptions, Post, Comment, Likes]:
        if not model.table_exists():
            model.create_table()
            print "Table {0} created - OK".format(model.__name__)
        else:
            print "Table {0} already exists".format(model.__name__)


def clear_db():
    for model in [Person, PersonSubscriptions, Post, Comment, Likes]:
        if model.table_exists():
            model.drop_table()
        model.create_table()
        print "Table '{0}' re-created - OK".format(model.__name__)
