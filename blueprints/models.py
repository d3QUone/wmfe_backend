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
    recovery_code = db.CharField()


class Meal(BaseModel):
    iikoid = db.CharField(unique=True, primary_key=True)


class Post(BaseModel):
    post_id = db.PrimaryKeyField()
    author = db.ForeignKeyField(Person, related_name="Post", on_delete="CASCADE", on_update="CASCADE")
    text = db.TextField()
    date = db.DateTimeField(default=datetime.datetime.now)
    # geotag = db.BlobField()
    likes = db.IntegerField(default=0)
    is_deleted = db.BooleanField(default=False)
    # is_in_favourites = db.BooleanField(default=False)
    # is_selfliked

class PostMeal(BaseModel):
    post = db.ForeignKeyField(Post, related_name="PostMeal", on_delete="CASCADE", on_update="CASCADE")
    meal = db.ForeignKeyField(Meal, related_name="PostMeal", on_delete="CASCADE", on_update="CASCADE")


class Likes(BaseModel):
    person = db.ForeignKeyField(Person, related_name="Likes", on_delete="CASCADE", on_update="CASCADE")
    post = db.ForeignKeyField(Post, related_name="Likes", on_delete="CASCADE", on_update="CASCADE")
    is_deleted = db.BooleanField(default=False)


# class Favourites(BaseModel):
#     person_id = db.ForeignKeyField(Person, related_name="Favourites", on_delete="CASCADE", on_update="CASCADE")
#     post_id = db.ForeignKeyField(Post, related_name="Favourites", on_delete="CASCADE", on_update="CASCADE")
#     is_deleted = db.BooleanField(default=False)


def init_database():
    for model in [Person, Meal, Post, PostMeal, Likes]:
        if not model.table_exists():
            model.create_table()
            print "Table {0} created - OK".format(model.__name__)
        else:
            print "Table {0} already exists".format(model.__name__)


def clear_db():
    for model in [Person, Meal, Post, PostMeal, Likes]:
        if model.table_exists():
            model.drop_table()
        model.create_table()
        print "Table '{0}' re-created - OK".format(model.__name__)
