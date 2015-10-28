
from flask_peewee import db
from flask_peewee.db import DoesNotExist


database = db.MySQLDatabase('<dbname>', **{'host': '127.0.0.1', 'password': '<password>', 'port': 5432, 'user': '<db_user>'})


class BaseModel(db.Model):
    class Meta:
        database = database


class Person(BaseModel):
    vkid = db.TextField(unique=True, primary_key=True)
    auth_cookie = db.TextField()
    recovery_code = db.TextField()


class Meal(BaseModel):
    iikoid = db.TextField(unique=True, primary_key=True)


class Post(BaseModel):
    post_id = db.IntegerField(primary_key=True)
